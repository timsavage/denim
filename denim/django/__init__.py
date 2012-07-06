# -*- encoding:utf8 -*-
from fabric.api import env, require, task
from denim import paths, system, utils


def manage(cmd, args='', revision=None, noinput=True, use_sudo=True, user=None):
    """
    Run a django manage.py command.

    :param cmd: the command to run.
    :param args: arguments to append.
    :param revision: version name that is being worked on.
    :param noinput: Do not ask for input.
    """
    with paths.cd_package(revision):
        utils.run_as('python manage.py %(cmd)s %(args)s' % {
            'cmd': cmd,
            'args': (' --noinput' if noinput else '') + args
        }, use_sudo, user)


def collectstatic(revision=None, noinput=True, use_sudo=True, user=None):
    """
    Collect static files.
    """
    manage('collectstatic', revision, noinput, use_sudo, user)


@task
def syncdb(revision=None, noinput=True, use_sudo=True, user=None):
    """
    Run a database sync
    """
    manage('syncdb', revision, noinput, use_sudo, user)


@task
def createsuperuser():
    """
    Run a database sync and migrate operation.
    """
    manage('createsuperuser', noinput=False)


def link_settings(revision=None, use_sudo=True, user=None):
    """
    Put correct settings in place.
    """
    require('deploy_env')
    system.create_symlink(
        paths.package_path(revision, 'deployment/settings_%(deploy_env)s.py' % env),
        paths.package_path(revision, 'local_settings.py'),
        use_sudo=use_sudo, user=user
    )
