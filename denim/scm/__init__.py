# -*- encoding:utf8 -*-
from fabric.api import env, task, require
from denim.environment import Proxy
from denim import utils


__proxy = Proxy('deploy_scm', globals(), 'hg')

tag = __proxy.method('tag', doc=
"""
Add a tag to the local repository.

:param comment: commit comment for the tag.
:param tag_name: name of the tag.

""")

archive = __proxy.method('archive', doc=
"""
Archive from local repository.

:param revision: revision to archive
:param out_file: name of file to output
:param sub_path: path within repository to archive
:param prefix: path prefix to apply to all files in archive.

""")

export_file = __proxy.method('export_file', doc=
"""
Retrieve a single file from a particular revision.

:param revision: revision to get file from
:param path: path to the file
:param out_file: output file name

""")

get_hash = __proxy.method('get_hash', doc=
"""
Obtain revisions hash code from local repository.

:param revision: revision to get hash of.

""")

get_revision_name = __proxy.method('get_revision_name', doc=
"""
Obtain revisions name from local repository.

:param revision: revision to generate name from.

This differs from :ref:`get_hash` in that a hash will only be returned for
revisions that are not unique (eg "default" for Mercurial).

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
    release_tag = 'release-' + version

    tag('Release ' + version, release_tag)
    print('Release tag:\t%s' % release_tag)
    return release_tag


@__proxy.local_method
def archive_app(revision, out_file=None):
    """
    Create an archive or the app folder for deployment.

    :param revision: Revision to deploy.
    :param out_file: Optional name of the archive file.
    :return: (path of generated file, deployed_revision).

    If the requested revision is a default revision (i.e. master for GIT or
    default for Mercurial the deployed_revision will be the hash code. This is
    to ensure that any deployment of code is always unique as defined by your
    source control system.

    """
    revision_name = get_revision_name(revision)
    if not out_file:
        require('package_name')
        out_file = '%s-%s.tar' % (env.package_name, revision_name)
    elif not out_file.endswith('.tar'):
            out_file += '.tar'

    archive(revision, out_file, 'app', prefix='./')
    return out_file, revision_name

__all__ = __proxy.methods
