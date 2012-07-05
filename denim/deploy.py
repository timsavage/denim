# -*- encoding:utf8 -*-
from fabric.api import put
from denim import scm, paths, utils


def archive_and_upload(revision, use_sudo=True, user=None):
    """
    Upload application archive based on a source control revision.
    :param revision: revision to deploy.
    """
    archive_file = scm.archive_app(revision)
    put(archive_file, '/tmp/%s' % archive_file)
    with paths.cd('app'):
        utils.run_as('tar -xzf /tmp/%s' % archive_file, use_sudo, user)
