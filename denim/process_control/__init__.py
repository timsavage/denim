# -*- encoding:utf8 -*-
"""
Methods for managing configuration of your process control system.

An alternative process controller can be selected by settings the:
``deploy_process_control`` env variable.

Options:
- supervisor (default)

"""
from denim._env_proxy import Proxy


__proxy = Proxy('deploy_process_control', globals(), 'supervisor')

## Config Management ##################

upload_config = __proxy.method('upload_config', doc=
"""
Upload configuration file.
""")

__all__ = __proxy.methods
