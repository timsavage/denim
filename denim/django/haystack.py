# -*- encoding:utf8 -*-
from fabric import colors
from fabric.api import task
from denim import django


@task
def reindex(revision=None):
    """
    Run a reindex operation on Haystack search indexes.

    :param revision: Revision to run operation on.

    """
    django.manage('reindex')
