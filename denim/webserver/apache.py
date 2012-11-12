# -*- encoding:utf8 -*-
from fabric.api import sudo
from denim import utils


def upload_config(name_prefix=None):
    raise NotImplemented


def enable_config(name_prefix=None):
    raise NotImplemented


def disable_config(name_prefix=None):
    raise NotImplemented


def test_config():
    utils.run_as('/usr/sbin/apache2ctl configtest', use_sudo=True)


def start():
    utils.run_as('/etc/init.d/apache2 start', use_sudo=True)


def stop():
    utils.run_as('/etc/init.d/apache2 stop', use_sudo=True)


def restart(check_config=True):
    if check_config:
        test_config()
    utils.run_as('/etc/init.d/apache2 restart', use_sudo=True)


def reload(check_config=True):
    if check_config:
        test_config()
    utils.run_as('/etc/init.d/apache2 reload', use_sudo=True)
