from fabric.api import run, sudo

__all__ = ('run_as', )


def run_as(command, use_sudo=False, user=None, **kwargs):
    """
    A wrapper around run and sudo that allows a user to be provided.

    :command: command to run as.
    :use_sudo: run this command with sudo; default is False.
    :user: if using sudo run command as this user; default None (root).
    """
    if use_sudo:
        return sudo(command, user=user, **kwargs)
    else:
        return run(command, **kwargs)
