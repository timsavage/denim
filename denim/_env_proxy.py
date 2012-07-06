# -*- encoding:utf8 -*-
from fabric import api


class Proxy(object):
    """
    Class to automate the proxying of modules. This is used so to allow
    projects to specify what tools they use within a project ie: Define the
    source control as GIT.
    """
    def __init__(self, key, globals, default=None):
        self.key = key
        self.default = default
        self._globals = globals
        self._module_cache = {}
        self._methods = set()

    def get_env_module(self):
        """
        Get the module defined in environment.
        """
        module_name = api.env.get(self.key, self.default)
        if not module_name:
            api.abort('The following required environment variable was not defined: %s' % self.key)
        module = self._module_cache.get(module_name)
        if not module:
            try:
                module = __import__(module_name, globals=self._globals,
                    fromlist=self.methods)
            except ImportError:
                api.abort('The following module defined in the environment variable "%s" does not exist: %s' % (self.key, module_name))
            else:
                self._module_cache[module_name] = module
        return module

    def get_env_method(self, name):
        """
        Get method from module defined in environment.
        :param name: name of the method.
        """
        module = self.get_env_module()
        try:
            return getattr(module, name)
        except AttributeError:
            api.abort('The method "%s" is not supported by "%s".' % (name, module.__name__))

    def method(self, name, task=False, doc=None):
        """
        Define a method.

        :param name: name of the method to proxy.
        :param task: apply fabric @task decorator to method.
        :param doc: doc string to use when proxying method.
        """
        self._methods.add(name)

        # Method wrapper that does redirection
        def wrapper(proxy, name):
            def _proxy(*args, **kwargs):
                method = proxy.get_env_method(name)
                return method(*args, **kwargs)
            return _proxy

        proxy = wrapper(self, name)
        proxy.__doc__ = doc
        proxy.__name__ = name

        if task:
            return api.task(proxy)
        else:
            return proxy

    def local_method(self, method):
        """
        Helper for defining local methods (adds to the method array)
        :param method:
        :return:
        """
        self._methods.add(method.__name__)
        return method

    @property
    def methods(self):
        return tuple(self._methods)
