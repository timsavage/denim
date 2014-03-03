# -*- coding: utf-8 -*-
from denim.constants import RootUser
from denim import pip
from tests._utils import ApiTestCase


class TestPip(ApiTestCase):
    def test_pip_install_requirements_default(self):
        pip.install_requirements()

        self.assertSudo('pip install --upgrade -r /opt/test-project/current/requirements.txt', user=RootUser)

    def test_pip_install_requirements_no_upgrade_specified_path(self):
        pip.install_requirements(upgrade=False, path_to_requirements='/tmp/requirements.txt')

        self.assertSudo('pip install -r /tmp/requirements.txt', user=RootUser)
