# -*- encoding:utf8 -*-
"""
Helpers for creating and activating a python virtualenv.

>>> # Create a virtual env
>>> create('/opt/mysite/')

>>> # Activate an use a virtualenv
>>> with activate():
>>>     pip.install_requirements()

"""
from fabric.api import prefix

from denim import utils
from denim import paths


__all__ = ('create', 'activate')


def create(path=None, python=None, system_site_packages=False, extra_options=None, use_sudo=True, user=None):
    """
    Create a python virtual environment.

    :param path: location to create virtualenv; default is the project path.
    :param python: specify a specific version of python.
    :param system_site_packages: use the system site packages flag.
    :param extra_options: additional options for virtualenv (see virtualenv documentation for description of options)
    :param use_sudo: run this command with sudo; default is True.
    :param user: when using sudo run as this user; default is None (or root).

    """
    if not path:
        path = paths.project_path()
    options = extra_options if extra_options else []
    if python:
        options.append('--python="%s"' % python)
    if system_site_packages:
        options.append('--system-site-packages')
    options.append(path)
    utils.run_as('virtualenv %s' % ' '.join(options), use_sudo=use_sudo, user=user)


def activate(path=None):
    """
    Context manager to enable a virtualenv.

    :param path: location of the virtualenv to activate; default is the project path.

    """
    if not path:
        path = paths.project_path()
    return prefix('source %s' % paths.join_paths(path, 'bin/activate'))
