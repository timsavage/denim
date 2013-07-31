# -*- encoding:utf8 -*-
from fabric.api import prefix
from denim import utils
from denim import paths

__all__ = ('create', 'activate')


def create(path=None, system_site_packages=False, use_sudo=True, user=None):
    """
    Create a virtual environment.

    :param path: location to create virtual env; default is deploy path.
    :param system_site_packages: use the system site packages flag.
    :param use_sudo: run this command with sudo; default is True.
    :param user: when using sudo run as this user; default is None (or root).

    """
    if not path:
        path = paths.deploy_path()
    options = []
    if system_site_packages:
        options.append('--system-site-packages')
    options.append(path)
    utils.run_as('virtualenv %s' % ' '.join(options), use_sudo=use_sudo, user=user)


def activate(path=None):
    """
    Context manager to enable a virtual env.

    :param path: location of the virtual env to activate; default is deploy path.

    """
    if not path:
        path = paths.deploy_path()
    return prefix('source %s' % paths.join_paths(path, 'bin/activate'))
