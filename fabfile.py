from fabric.api import *


@task
def test(with_coverage=False):
    """
    Run denim unit tests. Pass True to enable coverage.
    """
    if with_coverage:
        local('nosetests -w tests --all-modules --with-coverage --cover-package denim')
    else:
        local('nosetests -w tests --all-modules')
