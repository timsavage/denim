# -*- encoding:utf8 -*-
from datetime import date
from fabric.api import run, sudo, settings, hide
from denim.constants import RootUser, DeployUser

__all__ = ('run_as', 'generate_version')


def run_as(command, use_sudo=False, user=RootUser, **kwargs):
    """
    A wrapper around run and sudo that allows a user to be provided.

    :param command: command to run as.
    :param use_sudo: run this command with sudo; default is False.
    :param user: if using sudo run command as this user; default None (root).

    """
    if user is RootUser or user is DeployUser:
        user = user.sudo_identity()

    if use_sudo:
        return sudo(command, user=user, **kwargs)
    else:
        return run(command, **kwargs)


def generate_version(increment=None):
    """
    Generate a version number based on today's date and an optional increment.

    Version string is in the format %Y.%m.%d.increment.

    """
    version = date.today().strftime('%Y.%m.%d')
    if increment:
        try:
            version += '.{0}'.format(int(increment))
        except ValueError:
            raise ValueError("Increment must be an integer value.")
    return version


def run_test(command, hide_groups=('warnings', ), use_sudo=False, user=None):
    """
    Helper method for performing commands where the result is going to be
    tested. By default fabric will abort when a command returns a non 0 exit
    code.

    :param command: command to run.
    :param hide_groups: output groups to hide (by default hides warnings).
    :param use_sudo: run this command with sudo; default is False.
    :param user: if using sudo run command as this user; default None (root).
    :return: result of command as returned by `run` or `sudo` Fabric commands.
    """
    with settings(warn_only=True):
        with hide(*hide_groups):
            return run_as(command, use_sudo, user)
