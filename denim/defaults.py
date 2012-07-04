# -*- encoding:utf8 -*-
"""
The default provision and deployment strategy.

Provision
=========

- Create system user
- Create folder layout
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

def standard_provision():
    """

    """
    pass


def standard_deploy(revision):
    """

    """
    pass