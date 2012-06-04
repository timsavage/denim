"""
Methods for managing configuration and web-server processes.

An alternative web-server can be selected by settings the:

``deploy_web_server`` env variable.

Options:
- nginx (default)
- apache

"""
from denim._env_proxy import Proxy


__proxy = Proxy('deploy_web_server', globals(), 'nginx')

## Config Management ##################

upload_config = __proxy.method('upload_config', doc=
"""
Upload configuration file.

Configuration is loaded from:

  PROJECT_ROOT/conf/%(deploy_web_server)s/%(deploy_env)s.conf

and uploaded to correct configuration location for your particular web-server.

Often configuration is then required to be enabled.

""")

enable_config = __proxy.method('enable_config', doc=
"""
Enable web-server configuration.

""")

disable_config = __proxy.method('disable_config', doc=
"""
Disable web-server configuration.

""")

test_config = __proxy.method('test_config', doc=
"""
Test web-server configuration

""")


## Process Management #################

start = __proxy.method('start', task=True, doc=
"""
Start web-server

""")

stop = __proxy.method('stop', task=True, doc=
"""
Stop web-server

""")

restart = __proxy.method('restart', task=True, doc=
"""
Restart web-server

:check_config: check that web-servers configuration is correct before restarting.

""")

reload = __proxy.method('reload', doc=
"""
Reload web-server

:check_config: check that web-servers configuration is correct before restarting.

""")

__all__ = __proxy.methods
