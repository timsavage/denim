# -*- encoding:utf8 -*-
from fabric.api import *
from denim import (paths, system, utils)

SERVICE_NAME = 'nginx'


def upload_config(name_prefix=None):
    put(
        paths.local_config_file(SERVICE_NAME, name_prefix),
        paths.remote_config_file('/etc/nginx/sites-available', name_prefix),
        use_sudo=True,
    )

def enable_config(name_prefix=None):
    system.create_symlink(
        paths.remote_config_file('/etc/nginx/sites-available', name_prefix),
        paths.remote_config_file('/etc/nginx/sites-enabled', name_prefix),
        use_sudo=True,
    )


def disable_config(name_prefix=None):
    system.remove_file(
        paths.remote_config_file('/etc/nginx/sites-enabled', name_prefix),
        use_sudo=True,
    )


def test_config():
    result = utils.run_test('/usr/sbin/nginx -t', use_sudo=True)
    return result.succeeded


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
