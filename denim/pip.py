from denim import paths, utils

__all__ = ('install_requirements', )


def install_requirements(path_to_requirements=None, revision=None, *args, **kwargs):
    """
    Install requirements with PIP.

    To install into a virtualenv use the vitualenv.activate context manager.

    :path_to_requirements: path to requirements file; default is:
        `*deploy_path*/app/*revision*/requirements.txt`
    :revision: A specific revision name.

    """
    if not path_to_requirements:
        path_to_requirements = paths.package_path(revision, 'requirements.txt')

    utils.run_as('pip install -r %s' % path_to_requirements, *args, **kwargs)
