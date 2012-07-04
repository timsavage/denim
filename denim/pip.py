from fabric.api import run, sudo, env
import paths


def install_requirements(path_to_requirements=None, revision=None, use_sudo=False, user=None):
    """
    Install requirements with PIP.

    To install into a virtualenv use the vitualenv.activate context manager.

    :path_to_requirements: path to requirements file; default is *deploy_path*/src/*revision*/requirements.txt
    :revision: A specific revision name.

    """
    if not path_to_requirements:
        path_to_requirements = paths.package_path(revision, 'requirements.txt')

