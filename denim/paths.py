# -*- encoding:utf8 -*-
import posixpath
import os
from fabric.api import env, cd, require, abort


## Utils ####################

def join_paths(a, *p):
    """
    Joins multiple paths land ensures that the '/' is removed from the end.

    Any path in *p that starts with / will be have the / removed.

    """
    p = map(lambda i: i.lstrip('/'), p)
    return posixpath.join(a, *p).rstrip('/')


## Known paths ##############

def deploy_path(sub_path=None):
    """
    Deployment root path, the root of the deployment structure.

    :param sub_path: A path below the package path.

    """
    require('project_name')
    deploy_path_root = env.get('deploy_path_root', '/opt/webapps')
    return join_paths(deploy_path_root, env.project_name,
        sub_path if sub_path else '')


def package_path(revision=None, sub_path=None):
    """
    Package path, the path were the python application package is deployed to.

    Uses a number of fall-backs to get the current path.

    :param revision: A specific revision name.
    :param sub_path: A path below the package path.

    """
    if not revision:
        revision = env.get('revision', 'current')
    return deploy_path(join_paths('app', revision,
        sub_path if sub_path else ''))


def log_path():
    """
    Path where log files are located.

    """
    require('project_name', 'package_name')
    log_path_root = env.get('log_path_root', '/var/log/webapps')
    return join_paths(log_path_root, env.project_name, env.package_name)


def wsgi_socket_path():
    """
    Path of WSGI socket, this is used to connect web-server to application.

    """
    return deploy_path('var/wsgi.sock')


def remote_config_file(base_path, name_prefix=None, extension='.conf'):
    """
    Determine the correct remote config file path.

    :param base_path: location of the config file on remote file system.
    :param name_prefix: an optional prefix for the configuration file name.
    :param extension: file extension of config files.

    """
    require('project_name')
    path_elements = {
        'name': env.project_name,
        'prefix': name_prefix,
        'ext': extension,
    }
    if name_prefix:
        return join_paths(base_path, '%(prefix)s-%(name)s%(ext)s' % path_elements)
    else:
        return join_paths(base_path, '%(name)s%(ext)s' % path_elements)


## Local paths ##############

def join_local_paths(a, *p):
    """
    Joins multiple paths and ensures that there is no path separator on the
    end.

    Any path in *p that starts with a separator will be have the separator
    removed.

    """
    p = map(lambda i: i.lstrip(os.path.sep), p)
    return os.path.normpath(os.path.join(a, *p).rstrip(os.path.sep))


def local_path(sub_path=None):
    """
    Local path relative to current fabfile.

    :param sub_path: local sub path relative to current fabfile.

    """
    require('real_fabfile')
    fabfile_path = os.path.dirname(env.real_fabfile)
    return join_local_paths(fabfile_path, sub_path if sub_path else '')


def local_working_path(sub_path=None, file_name=None, ensure_exists=True):
    """
    Path to a local working path.

    This path can be changed from the default `den` via the fabric environment
    parameter `working_path`.

    :param sub_path: sub path within working directory.
    :param file_name: optional file name within directory (this is a separate
        option to allow the `ensure_exists` flag to work correctly).
    :param ensure_exists: ensures that the path exists.

    """
    path = local_path(env.get('working_path', 'den'))
    if sub_path:
        path = join_local_paths(path, sub_path)
    if ensure_exists and not os.path.exists(path):
        os.makedirs(path)

    if file_name:
        return join_local_paths(path, file_name)
    else:
        return path


def local_config_file_options(service_name, name_prefix=None,
                              extension='.conf'):
    """
    Local names of a service config file with fallbacks.

    Will return the name as well as optional fallback names for environment
    specific configuration.

    :param service_name: name of the service the configuration files is for.
    :param name_prefix: an optional prefix for the configuration file name.
    :param extension: file extension of config files.

    Names of config files follow the following convention:

      [
        FABFILE_PATH/conf/SERVICE_NAME/ENVIRONMENT.EXTENSION,
        FABFILE_PATH/conf/SERVICE_NAME.EXTENSION,
      ]

    or with a prefix:

      [
        FABFILE_PATH/conf/SERVICE_NAME/PREFIX-ENVIRONMENT.EXTENSION
        FABFILE_PATH/conf/SERVICE_NAME/ENVIRONMENT.EXTENSION,
        FABFILE_PATH/conf/PREFIX-SERVICE_NAME.EXTENSION,
        FABFILE_PATH/conf/SERVICE_NAME.EXTENSION,
      ]

    """
    require('deploy_env')
    path_elements = {
        'name': service_name,
        'prefix': name_prefix,
        'env': env.deploy_env,
        'ext': extension,
    }
    if name_prefix:
        return [
            local_path('conf/%(name)s/%(prefix)s-%(env)s%(ext)s' % path_elements),
            local_path('conf/%(name)s/%(env)s%(ext)s' % path_elements),
            local_path('conf/%(prefix)s-%(name)s%(ext)s' % path_elements),
            local_path('conf/%(name)s%(ext)s' % path_elements),
        ]
    else:
        return [
            local_path('conf/%(name)s/%(env)s%(ext)s' % path_elements),
            local_path('conf/%(name)s%(ext)s' % path_elements),
        ]


def local_config_file(service_name, name_prefix=None, abort_if_not_found=True,
                      extension='.conf'):
    """
    Determine the correct local config file, this method will try several
    options as resolved by `local_config_file_options` and return the path to
    the first matching file that exists on disk.

    :param service_name: name of the service the configuration files is for.
    :param name_prefix: an optional prefix for the configuration file name.
    :param abort_if_not_found: abort fabric operation if the requested file
        could not be found.
    :param extension: file extension of config files.

    """
    file_options = local_config_file_options(service_name, name_prefix, extension)
    for file_option in file_options:
        if os.path.exists(file_option):
            return file_option
    if abort_if_not_found:
        abort("""
Not able to find a configuration file for service "%s".

Searched path(s): %s
""" % (service_name, file_options))


## Context managers #########

def cd_deploy(*args, **kwargs):
    """
    Context manager to change to the deploy path.

    :sub_path: A path below the package path.

    """
    return cd(deploy_path(*args, **kwargs))


def cd_package(*args, **kwargs):
    """
    Context manager to change to a package path.

    :revision: Name of revision; default is *env.revision* or *current*.
    :sub_path: A path within the package.

    """
    return cd(package_path(*args, **kwargs))
