from denim import *

## Configuration ######################

# Name of the project
env.project_name = 'Denim'

# Name of the application package
env.package_name = 'denim_demo'

# Override default source control management tool
# env.deploy_scm = 'hg' # Options 'git', 'hg'

# Override default web-server
# env.deploy_web_server = 'nginx' # Options 'apache', 'nginx'


## Deployment environments ############

@task(alias='prod')
def production():
    env.deploy_env = 'production'
    env.hosts = ['192.168.1.10', '192.168.1.12']

@task
def staging():
    env.deploy_env = 'staging'
    env.hosts = ['192.168.2.10', '192.168.2.12']


## Actions ############################

@task
def provision():
    default.standard_provision()

@task(alias='d')
def deploy(revision):
    default.standard_deploy(revision)
