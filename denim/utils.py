# -*- encoding:utf8 -*-
from datetime import date
from fabric.api import run, sudo

__all__ = ('run_as', 'generate_version')


def run_as(command, use_sudo=False, user=None, **kwargs):
    """
    A wrapper around run and sudo that allows a user to be provided.

    :param command: command to run as.
    :param use_sudo: run this command with sudo; default is False.
    :param user: if using sudo run command as this user; default None (root).

    """
    if use_sudo:
        return sudo(command, user=user, **kwargs)
    else:
        return run(command, **kwargs)


def generate_version(revision=None):
    """
    Generate a version number based on today's date and an optional revision.

    Version string is in the format %Y.%m.%d.revision.

    """
    version = date.today().strftime('%Y.%m.%d')
    if revision:
        try:
            version += '.{0}'.format(int(revision))
        except ValueError:
            raise ValueError("Revision must be an integer value.")
    return version
