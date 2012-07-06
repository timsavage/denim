# -*- encoding:utf8 -*-
from fabric.api import *
from denim import paths

SERVICE_NAME = 'supervisor'


def upload_config(name_prefix=None):
    """
    Upload configuration file.

    :param name_prefix: Prefix to append to service name to provide alternate
        configuration (or support multiple services)

    """
    put(
        paths.local_config_file(SERVICE_NAME, name_prefix),
        paths.remote_config_file('/etc/supervisor/conf.d', name_prefix),
        use_sudo=True
    )


def manager_start():
    """
    Start service manager.

    """
    sudo('/etc/init.d/supervisor start')


def manager_stop():
    """
    Stop service manager.

    """
    sudo('/etc/init.d/supervisor stop')


def manager_restart():
    """
    Restart service manager.

    """
    sudo('/etc/init.d/supervisor restart')


def manager_reload():
    """
    Reload service manager.

    """
    sudo('supervisorctl reread')


def start(service_name):
    """
    Start process.

    :param service_name: name of the service to start in supervisor.

    """
    sudo('supervisorctl start %s' % service_name)


def stop(service_name):
    """
    Stop process.

    :param service_name: name of the service to stop in supervisor.

    """
    sudo('supervisorctl start %s' % service_name)


def restart(service_name):
    """
    Restart process.

    :param service_name: name of the service to restart in supervisor.

    """
    sudo('supervisorctl restart %s' % service_name)


def status(service_name):
    """
    Process status.

    :param service_name: name of the service to get status of.

    """
    sudo('supervisorctl status %s' % service_name)
