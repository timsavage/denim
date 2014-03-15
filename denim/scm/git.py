# -*- encoding:utf8 -*-
from denim.utils import local, escape_string


def commit(comment, file_name=None):
    """
    Commit into source control.

    :param comment: comment for commit
    :param file_name: name of file to commit. If not supplied will commit all
        files.

    """
    if file_name:
        local('git commit -m "%s" "%s"' % (escape_string(comment), file_name))
    else:
        local('git commit -m "%s"' % escape_string(comment))


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
    args.append(revision)
    args.append(sub_path)
    local('git archive %s > %s' % (' '.join(args), out_file))


def export_file(revision, path, out_file):
    """
    Retrieve a single file from a particular revision.

    :param revision: revision to get file from
    :param path: path to the file
    :param out_file: output file name

    """
    local('git show %s:%s > %s' % (revision, path, out_file))


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


def get_root():
    """
    Get the root path of the current repository.
    
    """
    return os.path.abspath(local("git rev-parse --show-cdup", capture=True))
