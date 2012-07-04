# -*- encoding:utf8 -*-
from fabric.api import env, task, require
from denim._env_proxy import Proxy
from denim import utils
from denim import paths


__proxy = Proxy('deploy_scm', globals(), 'hg')

tag = __proxy.method('tag', False, doc=
"""
Add a tag to the local repository.
""")

archive = __proxy.method('archive', False, doc=
"""
Archive from local repository.
""")


@task
@__proxy.local_method
def tag_release(increment='0'):
    """
    Tag release in repository.

    Release tags have the following format release-%Y.%m.%d.increment

    :param increment: Incremental release number.
    :return: The created revision
    """
    version = utils.generate_version(increment)
    tag(version)
    print('Tagged version:\t{0}\nRelease tag:\trelease-{0}'.format(version))
    return version


@__proxy.local_method
def archive_app(revision, out_file=None):
    """
    Create an archive or the app folder for deployment.

    :param revision: Revision to deploy.
    :param out_file: Optional name of the archive file.
    :return: path of generated file.
    """
    if not out_file:
        require('package_name')
        out_file = '%(package_name)s.tar.gz' % env
    archive(revision, out_file, 'app')
    return out_file

__all__ = __proxy.methods
