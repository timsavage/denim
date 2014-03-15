from denim.environment import EnvironmentCallableTask

__all__ = ('deploy_env', )


def deploy_env(*args, **kwargs):
    """
    Decorator declaring the wrapped function defines a deploy environment.

    May be invoked as a simple, argument-less decorator (i.e. ``@task``) or
    with arguments customizing its behavior (e.g. ``@task(alias='myalias')``).

    This decorator is essentially the same to the
    :ref:`new-style task <task-decorator>` see that decorator for details on
    how to use this decorator.

    """
    invoked = bool(not args or kwargs)
    task_class = kwargs.pop("task_class", EnvironmentCallableTask)
    if not invoked:
        func, args = args[0], ()

    def wrapper(func):
        return task_class(func, *args, **kwargs)

    return wrapper if invoked else wrapper(func)


class cached_property(object):  # noqa
    """
    Acts like a standard class `property` except return values cached.
    """
    def __init__(self, func):
        self.func = func
        self.__doc__ = func.__doc__
        self.__name__ = func.__name__
        self.__module__ = func.__module__

    def __get__(self, instance, owner):
        try:
            value = instance._cache[self.__name__]
        except (KeyError, AttributeError):
            value = self.func(instance)
            try:
                cache = instance._cache
            except AttributeError:
                cache = instance._cache = {}
            cache[self.__name__] = value
        return value
