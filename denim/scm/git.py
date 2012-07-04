# -*- encoding:utf8 -*-
from fabric.api import task, local
from denim.utils import generate_version


def tag_release(revision='0'):
  version = generate_version(revision)
  local('git tag -a -m "Release {0}" release-{0}'.format(version))
  print('Tagged version:\t{0}\nRelease tag:\trelease-{0}'.format(version))
  return version
