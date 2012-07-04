# -*- encoding:utf8 -*-
from fabric.api import local


def tag(version):
    local('hg tag -m "Release {0}" release-{0}'.format(version))


def archive(revision, out_file, sub_path, prefix=None):
    args = [
        '-r ' + revision,
        '-I ' + sub_path
    ]
    if prefix:
        args.append('-p ' + prefix)
    local('hg archive %s %s' % (' '.join(args), out_file))
