from fabric.api import *
import denim.paths


def upload_config(name_prefix=None):
    """
    Upload configuration for supervisor.

    :name_prefix: an optional prefix for the configuration file name.

    """
    source = denim.paths.get_local_config_path('supervisor', name_prefix=name_prefix)
    target = denim.paths.join_paths('/etc/supervisor/conf.d', '%(project_name)s.conf' % env)
    put(source, target, use_sudo=True)
