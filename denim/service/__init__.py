# -*- encoding:utf8 -*-
"""
Methods for managing configuration of your application service.

An alternative process controller can be selected by settings the:
``deploy_service_manager`` env variable.

Options:
- supervisor (default)

"""
from denim._env_proxy import Proxy


__proxy = Proxy('deploy_service_manager', globals(), 'supervisor')

## Config Management ##################

upload_config = __proxy.method('upload_config', doc=
"""
Upload configuration file.

:param name_prefix: Prefix to append to service name to provide alternate
    configuration (or support multiple services)
""")


## Service Management #################

start = __proxy.method('start', True, doc=
"""
Start process.

:param name_prefix: Prefix to append to service name to provide alternate
    configuration (or support multiple services)
""")

stop = __proxy.method('stop', True, doc=
"""
Stop process.

:param name_prefix: Prefix to append to service name to provide alternate
    configuration (or support multiple services)
""")

restart = __proxy.method('restart', True, doc=
"""
Restart process.

:param name_prefix: Prefix to append to service name to provide alternate
    configuration (or support multiple services)
""")

__all__ = __proxy.methods
