# -*- encoding:utf8 -*-
from fabric.api import env, require, task
from denim import paths, system, utils
from denim.constants import DeployUser


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
            'args': ('--noinput ' if noinput else '') + args
        }, use_sudo, user)


def test_deploy(revision=None):
    """
    Call manage.py validate to ensure deployment is working correctly.
    """
    manage('validate', '', revision, noinput=False)


def collectstatic(revision=None, use_sudo=True, user=DeployUser):
    """
    Collect static files.
    """
    manage('collectstatic', '', revision, use_sudo=use_sudo, user=user)


@task
def syncdb(revision=None, user=DeployUser, *args, **kwargs):
    """
    Run a database sync
    """
    manage('syncdb', '', revision, user=user, *args, **kwargs)


@task
def createsuperuser(username='', revision=None, user=DeployUser, *args, **kwargs):
    """
    Run a database sync and migrate operation.
    """
    manage('createsuperuser', username, revision, noinput=False, user=user, *args, **kwargs)


def link_settings(revision=None, use_sudo=True, user=None):
    """
    Put correct settings in place.
    """
    require('deploy_env')
    system.create_symlink(
        paths.package_path(revision, '%(package_name)s/deployment/settings_%(deploy_env)s.py' % env),
        paths.package_path(revision, '%(package_name)s/local_settings.py' % env),
        use_sudo=use_sudo, user=user
    )
