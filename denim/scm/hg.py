# -*- encoding:utf8 -*-
from denim.utils import local


def escape_string(value):
    return value.replace('"', '\\"')


def commit(comment, file_name=None):
    """
    Commit into source control.

    :param comment: comment for commit
    :param file_name: name of file to commit. If not supplied will commit all
        files.

    """
    if file_name:
        local('hg commit -m "%s" "%s"' % (escape_string(comment), file_name))
    else:
        local('hg commit -m "%s"' % escape_string(comment))


def tag(comment, tag_name):
    """
    Add a Mercurial tag to the local repository.

    :param comment: commit comment for the tag.
    :param tag_name: name of the tag.

    """
    local('hg tag -m "%s" %s' % (escape_string(comment), tag_name))


def archive(revision, out_file, sub_path, prefix=None):
    """
    Archive revision from Mercurial.

    :param revision: Revision to archive
    :param out_file: Name of file to output
    :param sub_path: Path within repository to archive
    :param prefix: Path prefix to apply to all files in archive.

    """
    args = [
        '-r ' + revision,
        '-I ' + sub_path
    ]
    if prefix:
        args.append('-p ' + prefix)
    local('hg archive %s %s' % (' '.join(args), out_file))


def export_file(revision, path, out_file):
    """
    Retrieve a single file from a particular revision.

    :param revision: revision to get file from
    :param path: path to the file
    :param out_file: output file name

    """
    local('hg cat -r %s %s > %s' % (revision, path, out_file))


def get_hash(revision):
    """
    Obtain revisions hash code from Mercurial.

    :param revision: revision to get hash of.

    """
    return local("hg id -i -r %s" % revision, capture=True)


def get_revision_name(revision):
    """
    Obtain revisions name from Mercurial.

    :param revision: revision to generate name from.

    This differs from :ref:`get_hash` in that a hash will only be returned for
    revisions that are not unique (eg "default" for Mercurial).

    """
    return get_hash(revision) if revision in ('default', ) else revision


def get_root():
    """
    Get root path of current HG repository.

    """
    return local("hg root", capture=True)
