from fabric.api import env, sudo, run, settings, hide
from fabric.contrib import files


def user_exists(user=None):
    """
    Check if a user exists.

    :user: name of the user to check; defaults to the deploy_user.

    """
    if not user:
        user_name = env.deploy_user

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

    :user: name of the user to create; defaults to the deploy_user.
    :home: path to home directory of user; defaults to deploy_path.

    :returns: True if user is created; else False to indicate user already exists.
    """
    if not user:
        user = env.deploy_user

    if not user_exists(user):
        sudo('adduser --system --quiet --home %(home)s %(user)s' % {
            'home': home if home else env.deploy_path,
            'user': user
        })
        return True
    else:
        return False

def change_owner(path, recursive=False, user=None):
    """
    Change the owner of a path.

    :path: to change owner of.
    :recursive: if the path references a folder recurs through all sub folders.
    :user: name of the user to make owner; defaults to the deploy_user.
    """
    if not user:
        user = env.deploy_user

    sudo('chown %s %s. %s' % (
        '-R' if recursive else '',
        user,
        path
    ))

def create_symlink(target_path, link_path, replace_existing=True, use_sudo=False):
    """
    Create a symlink on remote server.

    :target_path: target of symlink.
    :link_path: location of symlink.
    :replace_existing: overwrite an existing symlink; else fail if link already exists.
    :use_sudo: perform operation with sudo.
    """
    exe = sudo if use_sudo else run
    if replace_existing and files.exists(link_path):
        exe('rm "%s"' % link_path)
    exe('ln -s "%s" "%s"' % (target_path, link_path))
