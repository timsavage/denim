# -*- encoding:utf8 -*-
from fabric.api import env


class RootUser(object):
    """
    Class to define Root user.
    """
    uid=0

    @classmethod
    def sudo_identity(cls):
        return None


class DeployUser(object):
    """
    Class to define Deploy User.
    """

    @classmethod
    def sudo_identity(cls):
        return env.deploy_user
