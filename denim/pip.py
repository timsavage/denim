# -*- encoding:utf8 -*-
from fabric.api import env
from denim import paths, utils

__all__ = ('install_requirements', )


def install_requirements(path_to_requirements=None, revision=None, use_sudo=True, user=None):
    """
    Install requirements with PIP.

    To install into a virtualenv use the vitualenv.activate context manager.

    :path_to_requirements: path to requirements file; default is:
        `*deploy_path*/app/*revision*/requirements.txt`
    :revision: A specific revision name.

    """
    if not path_to_requirements:
        path_to_requirements = paths.package_path(revision, 'requirements.txt')
    if env.has_key('proxy'):
        utils.run_as('pip install --proxy=%s -r %s' % (env.proxy, path_to_requirements), use_sudo, user)
    else:
        utils.run_as('pip install -r {0}'.format(requirements_file))
