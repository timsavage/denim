# -*- encoding:utf8 -*-
from fabric import colors
from fabric.api import task, settings, hide
from denim import django

__all__ = ('show_migrations', 'migrate',)


@task
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
        django.manage('migrate', '--list', revision=revision, use_sudo=False)


@task
def migrate(revision=None):
    """
    Apply migrations.

    :param revision: revision of the application to run show migrations from.

    """
    django.manage('migrate', revision=revision, use_sudo=False)
