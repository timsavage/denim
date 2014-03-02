from fabric import api as _api

# Setup some default values.
_api.env.deploy_user = 'webapps'


@_api.task(name="help")
def show_help():
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


@_api.task
def environments():
    """
    Environments defined in fabfile.
    """
    from denim.environment import get_environments
    print 'Environments defined in fab file:'
    print ', '.join(get_environments())
