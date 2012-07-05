# -*- encoding:utf8 -*-
from fabric.api import env, require
from denim import paths, system, utils


def manage(cmd, args='', revision=None, noinput=True, use_sudo=True, user=None):
    """
    Run a django manage.py command.
    """
    with paths.cd_package(revision):
        utils.run_as('python manage.py %(cmd)s %(args)s' % {
            'cmd': cmd,
            'args': args + (' --noinput' if noinput else '')
        }, use_sudo, user)


def collectstatic(revision=None, noinput=True, use_sudo=True, user=None):
    """
    Collect static files.
    """
    manage('collectstatic', revision, noinput, use_sudo, user)


def syncdb(noinput=True, revision=None, use_sudo=True, user=None):
    """
    Run a database sync
    """
    manage('syncdb', revision, noinput, use_sudo, user)


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
