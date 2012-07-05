# -*- encoding:utf8 *-*
from fabric.api import *
from denim import paths, system

__all__ = ('create_default_layout',)


def create_default_layout():
    """
    Create default deployment layout.

    """
    deploy_path = paths.deploy_path()
    log_path = paths.log_path()

    # Create paths
    sudo('mkdir -p %s{app,public,var}' % deploy_path)
    sudo('mkdir -p %spublic/{media,static}' % deploy_path)
    sudo('mkdir -p %s' % log_path)

    # Set correct user for application writable paths.
    system.change_owner(paths.join_paths(deploy_path, 'var'))
    system.change_owner(paths.join_paths(deploy_path, 'public/media'))
    system.change_owner(log_path)
