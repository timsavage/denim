# -*- coding: utf-8 -*-
import boto.ec2


def get_connection():
    """
    Return connection (will reuse
    :return:
    """
    pass


def get_hosts(group):
    """
    Get a group of hosts in an AWS group (allows for deployment to dynamic groups of EC2 instances).

    :param group: name of the AWS group.
    :return: list of public DNS names.

    """
    pass