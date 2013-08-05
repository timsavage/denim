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
    return posixpath.join(a, *(i.lstrip('/') for i in p)).rstrip('/')


## Remote paths ##############

def deploy_path(sub_path=None):
    """
    Deployment root path on the remote host, this is the root path from which other paths are built.

    :param sub_path: A path below the package path.

    """
    require('project_name')
    deploy_path_root = env.get('deploy_path_prefix', '/opt/www')
    return join_paths(deploy_path_root, env.project_name, sub_path if sub_path else '')


def application_path(revision=None, sub_path=None):
    """
    Application path, the path were the python application package is deployed to.

    Format of the application path:

        DEPLOY_PATH/app/REVISION/SUB_PATH

    Where REVISION is replaced with "current" if no revision is defined (either passed into the method or defined by the
    current environment) and SUB_PATH is replaced with an empty string if no path is defined).

    :param revision: A specific revision name.
    :param sub_path: A path below the package path.

    """
    if not revision:
        revision = env.get('revision', 'current')
    return deploy_path(join_paths('app', revision, sub_path or ''))


def package_path(*args, **kwargs):
    import warnings
    warnings.warn("The package_path method has been deprecated in favour of application_path.",
                  category=DeprecationWarning)
    return application_path(*args, **kwargs)


def log_path():
    """
    Path where log files are located.

    """
    require('project_name', 'package_name')
    log_path_root = env.get('log_path_prefix', '/var/log/www')
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
    return os.path.normpath(os.path.join(a, *(i.lstrip('/') for i in p)).rstrip(os.path.sep))


def local_path(sub_path=None):
    """
    Local path relative to current fabfile.

    :param sub_path: local sub path relative to current fabfile.

    """
    require('real_fabfile')
    fabfile_path = os.path.dirname(env.real_fabfile)
    return join_local_paths(fabfile_path, sub_path or '')


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
    import warnings
    warnings.warn("This method should really make use of os.mktmp or similar.",
                  category=DeprecationWarning)

    path = local_path(env.get('working_path', 'den'))
    if sub_path:
        path = join_local_paths(path, sub_path)
    if ensure_exists and not os.path.exists(path):
        os.makedirs(path)

    if file_name:
        return join_local_paths(path, file_name)
    else:
        return path


SEARCH_PATHS = (
    'conf/%(name)s/%(env)s%(ext)s',
    'conf/%(name)s%(ext)s'
)
PREFIXED_SEARCH_PATHS = (
    'conf/%(name)s/%(prefix)s-%(env)s%(ext)s',
    'conf/%(name)s/%(env)s%(ext)s',
    'conf/%(prefix)s-%(name)s%(ext)s',
    'conf/%(name)s%(ext)s'
)


def _local_config_file_options(service_name, name_prefix=None, extension='.conf'):
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
    search_paths = PREFIXED_SEARCH_PATHS if name_prefix else SEARCH_PATHS
    for search_path in search_paths:
        yield local_path(search_path % path_elements)


def local_config_file(service_name, name_prefix=None, abort_if_not_found=True, extension='.conf'):
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
    searched_paths = []
    for path in _local_config_file_options(service_name, name_prefix, extension):
        if os.path.exists(path):
            return path
        searched_paths.append(path)
    if abort_if_not_found:
        abort("""
Not able to find a configuration file for service "%s".

Searched path(s): %s
""" % (service_name, searched_paths))


## Context managers #########

def cd_deploy(*args, **kwargs):
    """
    Context manager to change to the deploy path.

    :sub_path: A path below the package path.

    """
    return cd(deploy_path(*args, **kwargs))


def cd_application(*args, **kwargs):
    """
    Context manager to change to a application path.

    :revision: Name of revision; default is *env.revision* or *current*.
    :sub_path: A path within the application package.

    """
    return cd(application_path(*args, **kwargs))


def cd_package(*args, **kwargs):
    import warnings
    warnings.warn("The cd_package method has been deprecated in favour of cd_application.",
                  category=DeprecationWarning)
    return cd_application(*args, **kwargs)
