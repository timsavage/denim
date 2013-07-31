======
Django
======

.. py:module:: denim.django

.. py:function:: manage(cmd, [args='', revision=None, noinput=True, use_sudo=True, user=None])

    Run a django manage.py command.

    :param cmd: the command to run.
    :param args: arguments to append.
    :param revision: version name that is being worked on.
    :param noinput: Do not ask for input.


def collectstatic(use_sudo=True, user=DeployUser):
    """
    Collect static files.
    """
    manage('collectstatic', '', use_sudo=use_sudo, user=user)


@task
def syncdb(*args, **kwargs):
    """
    Run a database sync
    """
    manage('syncdb', '', *args, **kwargs)


@task
def createsuperuser(*args, **kwargs):
    """
    Run a database sync and migrate operation.
    """
    manage('createsuperuser', '', *args, **kwargs)


def link_settings(revision=None, use_sudo=True, user=None):