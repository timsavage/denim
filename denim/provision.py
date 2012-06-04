from fabric.api import *
import paths
import system


def create_default_layout():
    """
    Create default deployment layout.

    """
    deploy_path = paths.get_deploy_path()
    log_path = paths.get_log_path()

    # Create paths
    sudo('mkdir -p %s{app,public,var}' % deploy_path)
    sudo('mkdir -p %spublic/{media,static}' % deploy_path)
    sudo('mkdir -p %s' % log_path)

    # Set correct user for application writable paths.
    system.change_owner(paths.join_paths(deploy_path, 'var'))
    system.change_owner(paths.join_paths(deploy_path, 'public/media'))
    system.change_owner(log_path)
