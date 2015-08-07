# -*- encoding:utf8 -*-
import os
from fabric.api import env, put, require
from denim import paths, scm, utils


__all__ = ('install_requirements', )


def get_pip_cmd():
    return 'pip%s' % env.get('python_version', '')


def install_requirements(revision=None, path_to_requirements=None,
                         upgrade=True, use_sudo=True, user=None,
                         path_to_log=None):
    """
    Install requirements with PIP.

    To install into a virtualenv use the :ref:`vitualenv.activate` context
    manager.

    :path_to_requirements: path to requirements file; default is:
        `*release_path*/requirements.txt`
    :upgrade: when installing requirements fetch updates.
    :revision: A specific revision name.

    """
    if not path_to_requirements:
        path_to_requirements = paths.release_path(revision, 'requirements.txt')
    parameters = ['install']
    if 'proxy' in env:
        parameters.append('--proxy=%s' % env.proxy)
    if upgrade:
        parameters.append('--upgrade')
    if not path_to_log:
        path_to_log = paths.project_path('var/pip.log')
    parameters.append('-r %s' % path_to_requirements)
    utils.run_as('%s %s' % (get_pip_cmd(), ' '.join(parameters)), use_sudo, user)


def create_bundle_from_revision(revision, bundle_file=None):
    """
    Create pip bundle from requirements file.

    :param revision: Revision to bundle from.
    :param bundle_file: Name of bundle file; defaults to project name.

    Create bundle uses the following process to determine the what packages
    are to be bundled:

     - use `path_to_requirements`
     - use requirements.txt from app/requirements.txt@revision

    """
    require('project_name')

    if not bundle_file:
        bundle_file = paths.local_working_path(file_name='%s.pybundle' % revision)

    path_to_requirements = paths.local_working_path(file_name='%s-requirements.txt' % revision)
    scm.export_file(revision, 'app/requirements.txt', path_to_requirements)

    utils.local('%s bundle -r %s %s' % (get_pip_cmd(), path_to_requirements, bundle_file))
    return bundle_file


def install_bundle(bundle_file, use_sudo=True, user=None):
    """
    Install pip bundle.

    To install into a virtualenv use the :ref:`vitualenv.activate` context
    manager.

    :param bundle_file: path to bundle file

    """
    file_name = os.path.basename(bundle_file)
    remote_bundle = paths.join_paths('/tmp/', file_name)
    put(bundle_file, remote_bundle)
    utils.run_as('%s install %s' % (get_pip_cmd(), remote_bundle), use_sudo, user)
