from denim.constants import RootUser
from denim import system
from tests._utils import ApiTestCase


class TestSystem(ApiTestCase):
    def test_user_exists_default(self):
        system.user_exists()

        self.assertRun('id -u test')

    def test_user_exists_specified_user(self):
        system.user_exists('foo')

        self.assertRun('id -u foo')
