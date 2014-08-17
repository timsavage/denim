# -*- encoding:utf8 -*-
from fabric.api import env, require, task
from denim import paths, system, utils
from denim.constants import DeployUser


def manage(cmd, args=None, revision=None, noinput=True, use_sudo=True, user=DeployUser):
    """
    Run a django manage.py command.

    :param cmd: the command to run.
    :param args: arguments to append.
    :param revision: version name that is being worked on.
    :param noinput: Do not ask for input.

    """
    args = args or []
    if noinput:
        args.insert(0, '--noinput')
    args.insert(0, cmd)

    with paths.cd_package(revision):
        utils.run_as('python%s manage.py %s' % (env.get('python_version', 2), ' '.join(args)), use_sudo, user)


def test_deploy(revision=None):
    """
    Call manage.py validate to ensure deployment is working correctly.

    """
    manage('validate', revision=revision, noinput=False)


def collectstatic(revision=None, user=None):
    """
    Collect static files.

    """
    manage('collectstatic',
        revision=revision, user=user)


def syncdb(revision=None, **kwargs):
    """
    Run a database sync

    """
    manage('syncdb', revision=revision, **kwargs)


def createsuperuser(username='', revision=None, **kwargs):
    """
    Run a database sync and migrate operation.

    """
    manage('createsuperuser', [username], revision=revision, noinput=False, **kwargs)


def link_settings(revision=None, user=None, **kwargs):
    """
    Put correct settings in place.

    """
    require('deploy_env')
    system.create_symlink(
        paths.package_path(revision, '%(package_name)s/deployment/settings_%(deploy_env)s.py' % env),
        paths.package_path(revision, '%(package_name)s/local_settings.py' % env),
        user=user, **kwargs
    )
