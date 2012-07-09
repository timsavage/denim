# -*- encoding:utf8 -*-
"""
Methods for managing configuration and web-server processes.

An alternative web-server can be selected by settings the:

``deploy_web_server`` env variable.

Options:
- nginx (default)
- apache

"""
from fabric.api import abort
from denim.environment import Proxy


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

@__proxy.local_method
def install_config(name_prefix=None, disable_on_fail=True, abort_on_fail=True):
    """
    Install/enable and test configuration.

    :param name_prefix: name prefix for configuration.
    :param disable_on_fail: disable the configuration file on failure.
    :param abort_on_fail: abort script on failure.
    """
    upload_config(name_prefix)
    enable_config(name_prefix)
    result = test_config()
    if result:
        reload(check_config=False)
    else:
        if disable_on_fail:
            disable_config(name_prefix)
        if abort_on_fail:
            abort('Web server configuration test failed.')

__all__ = __proxy.methods
