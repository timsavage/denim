# -*- encoding:utf8 -*-
"""
Methods for managing OS packages.

An alternative package manager can be selected by settings the:
``deploy_package_manager`` env variable.

Note: Different distributions/operating systems have different naming
conventions for packages. For example Apache is referred to as apache on
Debian systems but httpd on Redhat systems.

Options:
- debian (default) Debian package management tools (apt, dpkg etc)

"""
from denim.environment import Proxy

__proxy = Proxy('deploy_package_manager', globals(), 'debian')

is_installed = __proxy.method(
    'is_installed', False,
    doc="""
    Check if a particular package has been installed.

    :param name: name of the package to check for.

    """
)

install = __proxy.method(
    'install', False,
    doc="""
    Install a package.

    :param name: name of the package to install.

    """
)


def ensure_installed(*package_names):
    """
    Install all packages in the list if they are not already installed.
    """
    for package_name in package_names:
        if package_name and not is_installed(package_name):
            install(package_name)


def check_installed(*package_names):
    """
    Check that certain packages are installed.

    Returns a list of packages that are not installed.
    """
    return [n for n in package_names if n and not is_installed(n)]

__all__ = __proxy.methods
