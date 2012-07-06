# -*- encoding:utf8 -*-
from fabric.api import local


def tag(comment, tag_name):
    """
    Add a Git tag to the local repository.

    :param comment: commit comment for the tag.
    :param tag_name: name of the tag.

    """
    local('git tag -a -m "%s" %s' % (comment, tag_name))


def archive(revision, out_file, sub_path, prefix=None):
    """
    Archive a revision from GIT.

    :param revision: Revision to archive
    :param out_file: Name of file to output
    :param sub_path: Path within repository to archive
    :param prefix: Path prefix to apply to all files in archive.

    """
    args = []
    if prefix:
        args.append('--prefix=' + prefix)
    local('git archive %s %s %s > %s' % (' '.join(args), revision, sub_path, out_file))


def get_hash(revision):
    """
    Obtain revisions hash code from GIT.

    :param revision: revision to get hash of.

    """
    return local("git log -1 --pretty=format:'%%H' %s" % revision, capture=True)


def get_revision_name(revision):
    """
    Obtain revisions name from GIT.

    :param revision: revision to generate name from.

    This differs from :ref:`get_hash` in that a hash will only be returned for
    revisions that are not unique (eg "master" for GIT).

    """
    return get_hash(revision) if revision in ('master', ) else revision
