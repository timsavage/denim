from denim._env_proxy import Proxy


__proxy = Proxy('deploy_scm', globals(), 'hg')

archive = __proxy.method('archive')

__all__ = __proxy.methods
