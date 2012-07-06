# -*- encoding:utf8 -*-
from fabric.api import sudo
from denim import utils


def is_installed(name):
    """
    Check if a particular package has been installed.

    :param name: name of the package to check for.
    """
    result = utils.run_test('dpkg --status "%s" | grep Status' % name)
    return result.succeeded


def install(name):
    """
    Install a package.

    :param name: name of the package to install.
    """
    sudo('apt-get install "%s"' % name)
