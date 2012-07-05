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
from fabric.api import sudo
from denim import deploy, paths, pip, system, virtualenv, webserver


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


def standard_provision():
    """

    """
    # Layout
    system.create_system_user()
    create_standard_layout()
    virtualenv.create()

    # Web server
    webserver.upload_config()
    webserver.enable_config()
    webserver.test_config()
    webserver.reload()

    # Process control



def standard_deploy(revision):
    """

    """
    deploy.archive_and_upload(revision)
    with virtualenv.activate():
        pip.install_requirements(revision, use_sudo=True)

