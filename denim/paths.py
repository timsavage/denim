import posixpath
import os.path
from fabric.api import env, cd, require


## Utils ####################

def join_paths(a, *p):
    """
    Joins multiple paths land ensures that the '/' is removed from the end.

    """
    return posixpath.join(a, *p).rstrip('/')


## Known paths ##############

def get_deploy_path(sub_path=None):
    """
    Path of deployment root.

    :sub_path: A path below the package path.

    """
    require('deploy_path', 'project_name')
    if sub_path:
        return join_paths(env.deploy_path, env.project_name, sub_path)
    else:
        return join_paths(env.deploy_path, env.project_name)

def get_package_path(revision=None, sub_path=None):
    """
    Get path to current package.

    Uses a number of fall-backs to get the current path.

    :revision: A specific revision name.
    :sub_path: A path below the package path.

    """
    if not revision:
        revision = env.get('revision', 'current')
    if not sub_path:
        sub_path = ''
    return get_deploy_path(join_paths('app', revision, sub_path))

def get_log_path():
    """
    Path to log files.

    """
    require('log_path_template', 'project_name', 'package_name')
    return env.log_path_template % env

def get_wsgi_socket():
    """
    Get the path to the WSGI socket used to connect webserver to application.

    """
    return get_deploy_path('var/wsgi.sock')


## Local paths ##############

def get_config_file_names(name_prefix=None):
    """
    Get names of config files.

    :name_prefix: an optional prefix for the configuration file name.

    :returns: (local_name, server_name)
    """
    require('deploy_env', 'project_name')
    name_prefix = (name_prefix + '-') if name_prefix else ''
    return (
        name_prefix + env.deploy_env + '.conf',
        name_prefix + env.project_name + '.conf',
    )

def get_local_path(sub_path=None):
    """
    Get local path relative to current fabfile.

    :sub_path: local sub path relative to current fabfile.

    """
    return os.path.join(env.real_fabfile, sub_path if sub_path else '')

def get_local_config_path(service_name, name_prefix=None):
    """
    Get local path to the configuration file of a service.

    Names of config files follow the following convention:

      FABFILE_PATH/conf/%(service_name)s/%(deploy_env).conf

    or with a prefix:

      FABFILE_PATH/conf/%(service_name)s/%(prefix)s-%(deploy_env)s.conf

    :service_name: name of the service the configuration files is for.
    :name_prefix: an optional prefix for the configuration file name.
    """
    require('real_fabfile')
    return os.path.join(env.real_fabfile, 'conf', get_config_file_names(name_prefix)[0])


## Context managers #########

def cd_deploy(*args, **kwargs):
    """
    Context manager to change to the deploy path.

    :sub_path: A path below the package path.

    """
    return cd(get_deploy_path(*args, **kwargs))

def cd_package(*args, **kwargs):
    """
    Context manager to change to a package path.

    :revision: Name of revision; default is *env.revision* or *current*.
    :sub_path: A path within the package.

    """
    return cd(get_package_path(*args, **kwargs))

def cd_log():
    """
    Context manager to change to the log path.

    """
    return cd(get_log_path())
