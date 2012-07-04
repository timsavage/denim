# -*- encoding:utf8 -*-
"""
The default provision and deployment strategy.

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
from denim import deploy, webserver, virtualenv, pip, provision, system


def standard_provision():
    """

    """
    # Layout
    system.create_system_user()
    provision.create_default_layout()
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

