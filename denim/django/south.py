# -*- encoding:utf8 -*-
from fabric.api import task
from fabric import colors
from denim.django import manage


@task
def show_migrations(non_applied_only=False, revision=None):
    """
    Print report of migrations.

    :param non_applied_only: only show un-applied migrations.
    :param revision: revision of the application to run show migrations from.
    """
    if non_applied_only:
        result = manage('migrate', args='--list | grep -v "(\*)"', revision=revision, use_sudo=False)
        if result.find('( )') != -1:
            print(colors.red('*'*34))
            print(colors.red('* Migrations need to be applied! *'))
            print(colors.red('*'*34))
        else:
            print(colors.green('Migrations up to date.'))
    else:
        manage('migrate', '--list', revision=revision, use_sudo=False)
