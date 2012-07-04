# -*- encoding:utf8 -*-
from fabric.api import sudo


def upload_config(name_prefix=None):
    raise NotImplemented


def enable_config(name_prefix=None):
    raise NotImplemented


def disable_config(name_prefix=None):
    raise NotImplemented


def test_config():
    sudo('/usr/sbin/apache2ctl configtest')


def start():
    sudo('/etc/init.d/apache2 start')


def stop():
    sudo('/etc/init.d/apache2 stop')


def restart(check_config=True):
    if check_config:
        test_config()
    sudo('/etc/init.d/apache2 restart')


def reload(check_config=True):
    if check_config:
        test_config()
    sudo('/etc/init.d/apache2 reload')
