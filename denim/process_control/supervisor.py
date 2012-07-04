from fabric.api import *
from denim import paths

SERVICE_NAME = 'supervisor'


def upload_config(name_prefix=None):
    put(
        paths.local_config_file(SERVICE_NAME, name_prefix),
        paths.remote_config_file('/etc/supervisor/conf.d', name_prefix),
        use_sudo=True
    )
