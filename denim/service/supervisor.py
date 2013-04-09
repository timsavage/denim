# -*- encoding:utf8 -*-
from fabric import colors
from fabric.api import put, env
from denim import paths, utils

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
    Start service manager daemon.

    """
    utils.run_as('/etc/init.d/supervisor start', use_sudo=True)


def manager_stop():
    """
    Stop service manager daemon.

    """
    utils.run_as('/etc/init.d/supervisor stop', use_sudo=True)


def manager_restart():
    """
    Restart service manager daemon.

    """
    # Using run test as this method seems to return a status of 1
    utils.run_test('/etc/init.d/supervisor restart', use_sudo=True)


def manager_reload():
    """
    Reload service manager daemon.

    """
    utils.run_as('supervisorctl reload', use_sudo=True)


def manager_status():
    """
    Status of service manager daemon.

    """
    if utils.run_test('/etc/init.d/supervisor status', use_sudo=True):
        print colors.green("Service is Up")
    else:
        print colors.red("Service is Down")


def start(service_name=None):
    """
    Start process.

    :param service_name: name of the service to start in supervisor.

    """
    if not service_name:
        service_name = env.project_name
    utils.run_as('supervisorctl start %s' % service_name, use_sudo=True)


def stop(service_name=None):
    """
    Stop process.

    :param service_name: name of the service to stop in supervisor.

    """
    if not service_name:
        service_name = env.project_name
    utils.run_as('supervisorctl stop %s' % service_name, use_sudo=True)


def restart(service_name=None):
    """
    Restart process.

    :param service_name: name of the service to restart in supervisor.

    """
    if not service_name:
        service_name = env.project_name
    utils.run_as('supervisorctl restart %s' % service_name, use_sudo=True)


def status(service_name=None):
    """
    Process status.

    :param service_name: name of the service to get status of.

    """
    if service_name is None:
        service_name = env.project_name
    utils.run_as('supervisorctl status %s' % service_name, use_sudo=True)
