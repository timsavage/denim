# -*- encoding:utf8 -*-
from datetime import date

from fabric import api as _api
from fabric.api import settings, hide

from denim.constants import RootUser


__all__ = ('run_as', 'run_test', 'local', 'generate_version')


class ApiWrapper(object):
    """
    An easily replaceable wrapper around api commands to allow for easy
    testing.
    """
    def sudo(self, command, **kwargs):
        return _api.sudo(command, **kwargs)

    def run(self, command, **kwargs):
        return _api.run(command, **kwargs)

    def local(self, command, **kwargs):
        return _api.local(command, **kwargs)


api = ApiWrapper()


def replace_api_wrapper(api_wrapper):
    global api
    api = api_wrapper


def run_as(command, use_sudo=False, user=RootUser, **kwargs):
    """
    A wrapper around run and sudo that allows a user to be provided.

    :param command: command to run as.
    :param use_sudo: run this command with sudo; default is False.
    :param user: if using sudo run command as this user; default None (root).

    """
    if hasattr(user, 'sudo_identity'):
        user = user.sudo_identity()

    if use_sudo:
        return api.sudo(command, user=user, **kwargs)
    else:
        return api.run(command, **kwargs)


def local(command, **kwargs):
    """
    A wrapper around the local command to push commands through the API
    wrapper to capture the output.

    :param command:

    """
    return api.local(command, **kwargs)


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


def generate_version(increment=None):
    """
    Generate a version number based on today's date and an optional increment.

    Version string is in the format %Y.%m.%d.increment.

    """
    version = date.today().strftime('%Y.%m.%d')
    if increment:
        try:
            version += 'r{0}'.format(int(increment))
        except ValueError:
            raise ValueError("Increment must be an integer value.")
    return version


def escape_string(value):
    """
    Escape a string for command line use.
    """
    return value.replace('"', '\\"')
