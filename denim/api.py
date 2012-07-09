from fabric import api as __api

# Setup some default values.
__api.env.deploy_user = 'webapps'

from denim.paths import (cd_deploy, cd_package, deploy_path, package_path)
from denim import (scm, service, system, virtualenv, webserver)
from denim.decorators import deploy_env


@__api.task
def help():
    """
    Help on common operations.
    """
    from denim.environment import get_environments

    print """
Common operations.

Provision server:
> fab {%(environments)s} init

Deploy (require a source control revision to be supplied. i.e. master):
> fab {%(environments)s} deploy:{revision}
""" % {
        'environments': '|'.join(get_environments()),
    }
