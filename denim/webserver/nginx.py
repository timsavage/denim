from fabric.api import *
import denim.paths
import denim.system


def _get_local_config(name_prefix):
    return denim.paths.get_local_config_path('nginx', name_prefix)

def _get_deploy_config(name_prefix, enabled=False):
    return denim.paths.join_paths('/etc/nginx/%s/')


def upload_config(name_prefix=None):
    source = denim.paths.get_local_path('conf/nginx/%(deploy_env)s.conf' % env)
    target = denim.paths.join_paths('/etc/supervisor/conf.d', '%(project_name)s.conf' % env)
    put(source, target, use_sudo=True)

def enable_config(name_prefix=None):
    source = denim.paths.join_paths('/etc/supervisor/conf.d', '%(project_name)s.conf' % env)
    target = denim.paths.get_local_path('conf/nginx/%(deploy_env)s.conf')
    raise NotImplemented

def disable_config(name_prefix=None):
    raise NotImplemented

def test_config():
    sudo('/usr/sbin/nginx -t')

def start():
    sudo('/etc/init.d/nginx start')

def stop():
    sudo('/etc/init.d/nginx stop')

def restart(check_config=True):
    if check_config:
        test_config()
    sudo('/etc/init.d/nginx restart')

def reload(check_config=True):
    if check_config:
        test_config()
    sudo('/usr/sbin/nginx -s reload')
