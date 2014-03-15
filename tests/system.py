from denim.constants import RootUser, DeployUser
from denim import system
from tests._utils import ApiTestCase


class TestSystem(ApiTestCase):
    def test_user_exists_default(self):
        system.user_exists()

        self.assertRun('id -u test')

    def test_user_exists_specified_user(self):
        system.user_exists('foo')

        self.assertRun('id -u foo')

    def test_change_owner(self):
        system.change_owner('/var/www', recursive=True, user=DeployUser)

        self.assertSudo('chown -R test. /var/www',
                        user=RootUser.sudo_identity())

    def test_change_mode(self):
        system.change_mode('/var/www', 0o755)

        self.assertSudo('chmod 755 /var/www',
                        user=RootUser.sudo_identity())
