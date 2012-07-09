# -*- encoding:utf8 -*-
from fabric.api import env, sudo, run, settings, hide
from fabric.contrib import files
from denim import paths, utils


def user_exists(user=None):
    """
    Check if a user exists.

    :param user: name of the user to check; defaults to the deploy_user.

    """
    if not user:
        user = env.deploy_user

    with settings(
        hide('warnings', 'running', 'stdout', 'stderr'),
        warn_only=True
    ):
        result = run('id -u %s' % user)

    return result.return_code == 0


def create_system_user(user=None, home=None):
    """
    Create a system user.

    If user already exists will ignore the operation.

    :param user: name of the user to create; defaults to the deploy_user.
    :param home: path to home directory of user; defaults to deploy_path.

    :return: True if user is created; else False to indicate user already
        exists.
    """
    if user is None:
        user = env.deploy_user
    if not user_exists(user):
        sudo('adduser --system --quiet --home %(home)s %(user)s' % {
            'home': home if home else paths.deploy_path(),
            'user': user
        })
        return True
    else:
        return False


def change_owner(path, recursive=False, user=None):
    """
    Change the owner of a path.

    :param path: to change owner of.
    :param recursive: if the path references a folder recurs through all sub
        folders.
    :param user: name of the user to make owner; defaults to the deploy_user.
    """
    if user is None:
        user = env.deploy_user
    sudo('chown %s %s. %s' % ('-R' if recursive else '', user, path))


def create_symlink(target_path, link_path, replace_existing=True,
                   *args, **kwargs):
    """
    Create a symlink on remote server.

    :param target_path: target of symlink.
    :param link_path: location of symlink.
    :param replace_existing: overwrite an existing symlink; else fail if link
        already exists.
    """
    if replace_existing:
        remove_file(link_path, *args, **kwargs)
    utils.run_as('ln -s "%s" "%s"' % (target_path, link_path), *args, **kwargs)


def remove_file(path, *args, **kwargs):
    """
    Remove a file from remote server.

    :param path: to file.
    :return: True if file existed and was removed else False

    """
    if not files.exists(path):
        return False
    utils.run_as('rm "%s"' % path, *args, **kwargs)
    return True
