# -*- encoding:utf8 -*-
from fabric import colors
from fabric.api import task, settings, hide
from denim import django
from denim.constants import DeployUser

__all__ = ('show_migrations', 'migrate',)


def show_migrations(revision=None, non_applied_only=False):
    """
    Print report of migrations.

    :param revision: revision of the application to run show migrations from.
    :param non_applied_only: only show un-applied migrations.

    """
    if non_applied_only:
        with settings(hide('warnings'), warn_only=True):
            result = django.manage('migrate', args='--list | grep -v "(\*)"', revision=revision, use_sudo=False)
        if result:
            if result.find('( )') != -1:
                print(colors.red('*'*34))
                print(colors.red('* Migrations need to be applied! *'))
                print(colors.red('*'*34))
            else:
                print(colors.green('Migrations up to date.'))
        else:
            print(colors.magenta('No migrations defined/or not using south.'))
    else:
        django.manage('migrate', ['--list'], revision=revision, use_sudo=False)


def migrate(migration=None, revision=None, user=DeployUser, **kwargs):
    """
    Apply migrations.

    :param revision: revision of the application to run show migrations from.
    :param migration: name of the migration to revert to, leave None to apply
        all migrations.

    """
    args = [migration] if migration else None
    django.manage('migrate', args, revision, user=user, **kwargs)

