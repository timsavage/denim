# -*- encoding:utf8 -*-
"""
Methods for managing configuration of your application service.

An alternative process controller can be selected by settings the:
``deploy_service_manager`` env variable.

Options:
- supervisor (default)

"""
from denim.environment import Proxy


__proxy = Proxy('deploy_service_manager', globals(), 'supervisor')

## Config Management ##################

upload_config = __proxy.method('upload_config', doc=
"""
Upload configuration file.

:param name_prefix: Prefix to append to service name to provide alternate
    configuration (or support multiple services)

""")

manager_start = __proxy.method('manager_start', task=True, doc=
"""
Start service manager daemon.

""")

manager_stop = __proxy.method('manager_stop', task=True, doc=
"""
Stop service manager daemon.

""")

manager_restart = __proxy.method('manager_restart', task=True, doc=
"""
Restart service manager daemon.

""")

manager_reload = __proxy.method('manager_reload', task=True, doc=
"""
Reload service manager daemon.

""")

manager_status = __proxy.method('manager_status', task=True, doc=
"""
Status of service manager daemon.

""")

## Service Management #################

start = __proxy.method('start', True, doc=
"""
Start process.

:param service_name: name of the service to start.

""")

stop = __proxy.method('stop', True, doc=
"""
Stop process.

:param service_name: name of the service to stop.

""")

restart = __proxy.method('restart', True, doc=
"""
Restart process.

:param service_name: name of the service to restart.

""")

status = __proxy.method('status', True, doc=
"""
Process status.

:param service_name: name of the service to get status of.

""")

@__proxy.local_method
def install_config(name_prefix=None):
    """
    Install configuration.

    :param name_prefix: name prefix for configuration.
    """
    upload_config(name_prefix)
    manager_restart()

__all__ = __proxy.methods
