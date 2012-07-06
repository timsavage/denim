# -*- encoding:utf8 -*-
"""
Common deployment recipes.

Provision
=========

- Create system user
- Create folder layout
- Create virtual env
- Deploy web-server configuration
- Test web-server configuration
- Reload web-server configuration
- Initial deployment
- Deploy init scripts

Deployment
==========

- Archive SCM release
- Upload and extract archive
- Install requirements

Django specific items
- Symlink Django environment specific settings
- Run collect static to migrate over content (also tests settings are correct)
- Display migrations that need to be run (south), warning only if south isn't present.

- Symlink new release as current

"""
from fabric import colors
from fabric.api import abort, put, require, sudo
from denim import (package, paths, pip, service, scm, system, utils,
                   virtualenv, webserver)


# These are the default packages for Nginx, PostgreSQL and Supervisor for
# Debian GNU/Linux or derivatives.
DEFAULT_PACKAGES = [
    'nginx', # Web server
    'supervisor', # Process Manager

    # Python requirements
    'python-virtualenv'
]


def archive_and_upload(revision, use_sudo=True, user=None):
    """
    Upload application archive based on a source control revision.

    :param revision: revision to deploy.
    :return: name of the revision that was deployed.

    """
    archive_file, revision_name = scm.archive_app(revision)
    put(archive_file, '/tmp/%s' % archive_file)
    with paths.cd_deploy('app'):
        utils.run_as('tar -xf /tmp/%s' % archive_file, use_sudo, user)
        utils.run_as('mv app %s' % revision, use_sudo, user)
    return revision_name


def create_standard_layout():
    """
    Create standard deployment layout.
    """
    deploy_path = paths.deploy_path()
    log_path = paths.log_path()

    # Create paths
    sudo('mkdir -p %s/{app,public,var}' % deploy_path)
    sudo('mkdir -p %s/public/{media,static}' % deploy_path)
    sudo('mkdir -p %s' % log_path)

    # Set correct user for application writable paths.
    system.change_owner(paths.join_paths(deploy_path, 'var'))
    system.change_owner(paths.join_paths(deploy_path, 'public/media'))
    system.change_owner(log_path)


def standard_provision(required_packages=DEFAULT_PACKAGES,
                       install_packages=True):
    """
    Standard provisioning recipe.

    :param required_packages: list of packages that are required on the server.
    :param install_packages: indicates if packages should be installed if they
        are not on the server.

    If `install_packages` is `False` and a package is missing provisioning will
    abort.
    """
    require('project_name', 'package_name', 'deploy_env')

    print colors.yellow("* Check correct packages are installed.")
    for package_name in required_packages:
        if not package.is_installed(package_name):
            if install_packages:
                package.install(package_name)
            else:
                abort('* Package "%s" is not available on the server.' % package_name)

    print colors.yellow("* Create standard layout.")
    system.create_system_user()
    create_standard_layout()
    virtualenv.create()

    print colors.yellow("* Upload configuration for dependant services.")
    print colors.yellow("** Web server.")
    webserver.install_config()
    print colors.yellow("** Service control.")
    service.install_config()


def standard_deploy(revision, use_pip_bundle=False):
    """
    Standard deployment recipe.

    :param use_pip_bundle: Create a pip bundle to install packages.

    """
    require('project_name', 'package_name', 'deploy_env')

    print colors.yellow("* Archive and upload requested revision.")
    deployed_revision = archive_and_upload(revision)

    with virtualenv.activate():
        print colors.yellow("* Install requirements.")
        if use_pip_bundle:
            bundle_file = pip.create_bundle_from_revision(deployed_revision)
            pip.install_bundle(bundle_file)
        else:
            pip.install_requirements(revision=deployed_revision, use_sudo=True)

