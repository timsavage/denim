# -*- encoding:utf8 -*-
from fabric.api import env


class UserBase(object):
    pass


class RootUser(UserBase):
    """
    Class to define Root user.
    """
    uid=0

    @classmethod
    def sudo_identity(cls):
        return None


class DeployUser(UserBase):
    """
    Class to define Deploy User.
    """

    @classmethod
    def sudo_identity(cls):
        return env.deploy_user
