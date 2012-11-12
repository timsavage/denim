from denim.constants import DeployUser
from denim.django import south
from tests._utils import ApiTestCase


class TestDjangoSouth(ApiTestCase):
    def test_south_migrate(self):
        south.migrate()

        self.assertSudo('python manage.py migrate --noinput',
            user=DeployUser.sudo_identity())

    def test_south_migrate_to_migration(self):
        south.migrate('0003')

        self.assertSudo('python manage.py migrate --noinput 0003',
            user=DeployUser.sudo_identity())

