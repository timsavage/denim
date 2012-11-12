# -*- encoding:utf8 -*-
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
    utils.run_as('apt-get install "%s"' % name, use_sudo=True)
