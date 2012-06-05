from denim._env_proxy import Proxy


__proxy = Proxy('deploy_scm', globals(), 'hg')

archive = __proxy.method('tag_release', True, doc=
"""
Add a tag to a GIT repository for a release.

Release tags have the following format release-%Y.%m.%d.revision

_usage_: fab scm.tag_release:1
"""
)

__all__ = __proxy.methods
