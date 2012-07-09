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
    import denim

    print """
Common operations with Denim (%(version)s).

Provision server:
> fab {%(environments)s} init

Deploy (require a source control revision to be supplied. i.e. master):
> fab {%(environments)s} deploy:{revision}

Status of service:
> fab {%(environments)s} service.status

""" % {
        'environments': '|'.join(get_environments()),
        'version': denim.__version__,
    }


@__api.task
def environment():
    """
    Environments defined in fabfile.
    """
    from denim.environment import get_environments
    print ','.join(get_environments())
