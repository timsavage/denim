# -*- encoding:utf8 -*-
from fabric.api import local, env


def tag(version):
    local('git tag -a -m "Release {0}" release-{0}'.format(version))


def archive(revision, out_file, sub_path, prefix=None):
    args = []
    if prefix:
        args.append('--prefix=' + prefix)
    local('git archive --format=tar %s %s %s > %s' % (' '.join(args), revision, sub_path, out_file))
