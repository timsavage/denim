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
from fabric.api import abort, env, put, require, sudo
from fabric.contrib.console import confirm
from fabric.contrib import files
from denim import (package, paths, pip, service, scm, system, utils,
                   virtualenv, webserver)
from denim.constants import RootUser


# These are the default packages for Nginx, PostgreSQL and Supervisor for
# Debian GNU/Linux or derivatives.
DEFAULT_PACKAGES = [
    'nginx', # Web server
    'supervisor', # Process Manager

    # Python requirements
    'python',
    'python-crypto',
    'python-virtualenv',
]


def archive_and_upload(revision, noinput=False, use_sudo=True, user=None):
    """
    Upload application archive based on a source control revision.

    :param revision: revision to deploy.
    :param noinput: do not ask for any input just take default action.
    :return: name of the revision that was deployed.

    """
    # Archive and upload package
    archive_file, revision_name = scm.archive_app(revision)
    put(archive_file, '/tmp/%s' % archive_file)

    with paths.cd_deploy('app'):
        # Extract package
        utils.run_as('tar -xf /tmp/%s' % archive_file, use_sudo, user)
        if files.exists(revision_name):
            if noinput or confirm(colors.red('This revision already exits on server, deploy over existing revision?')):
                utils.run_as('rm -rf %s' % revision_name, use_sudo, user)
            elif confirm('Terminate deployment?'):
                abort('Deployment terminated.')
            else:
                return revision_name
        utils.run_as('mv app %s' % revision_name, use_sudo, user)
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
    system.change_owner(paths.join_paths(deploy_path, 'public'), recursive=True)
    system.change_owner(log_path)


def standard_provision(extra_packages=[],
                       install_packages=True,
                       required_packages=DEFAULT_PACKAGES,):
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
    for package_name in required_packages + extra_packages:
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
    print colors.cyan("** Web server.")
    webserver.install_config()
    print colors.cyan("** Service control.")
    service.install_config()


def standard_deploy(revision, noinput=False,
                    use_pip_bundle=False):
    """
    Standard deployment recipe.

    :param revision: revision of the app to work on.
    :param noinput: do not ask for any input just take default action.
    :param use_pip_bundle: Create a pip bundle to install packages.

    """
    require('project_name', 'package_name', 'deploy_env')

    print colors.yellow("* Archive and upload requested revision.")
    env.revision = archive_and_upload(revision, noinput)

    with virtualenv.activate():
        print colors.yellow("* Install requirements.")
        if use_pip_bundle:
            bundle_file = pip.create_bundle_from_revision(env.revision)
            pip.install_bundle(bundle_file)
        else:
            pip.install_requirements(env.revision, use_sudo=True)

    return env.revision


def standard_django_deploy(noinput=False,
                           enable_south_migrations=True):
    """
    Standard django deployment

    :param noinput: do not ask for any input just take default action.
    :param revision: Do checks with south.

    .. note::
        This section assumes ``standard_deploy`` was run.

    """
    import django
    from django import south

    revision = env.revision

    with virtualenv.activate():
        print colors.yellow("* Setup Django deployment.")

        print colors.cyan("** Symlink in environment settings.")
        django.link_settings(revision)

        print colors.cyan("** Test deployment (./manage.py validate)..."),
        django.test_deploy(revision)
        print colors.green(' [OK]')

        print colors.cyan("** Collect static assets.")
        django.collectstatic(revision)

        if enable_south_migrations:
            print colors.cyan("** Display unapplied revisions")
            south.show_migrations(revision, True)
            msg = "Sync models and apply migrations?"
        else:
            msg = "Sync models?"

        if noinput or confirm(msg):
            print colors.cyan("** Syncing models")
            django.syncdb(revision)

            if enable_south_migrations:
                print colors.cyan("** Applying migrations")
                south.migrate(revision)


def standard_activate_deploy(noinput=False):
    """
    Standard activate recipe.

    :param noinput: do not ask for any input just take default action.

    .. note::
        This section assumes ``standard_deploy`` was run.

    """
    revision = env.revision

    print colors.yellow("* Make this deployment current.")
    print colors.cyan("** Symlinking to current")
    system.create_symlink(
        paths.package_path(revision),
        paths.package_path('current'),
        use_sudo=True, user=RootUser
    )

    print colors.cyan("** Restart service")
    service.restart()
