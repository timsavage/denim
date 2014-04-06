from denim.constants import RootUser
from tests._utils import ApiTestCase
from denim.package import debian


class TestPackageDebian(ApiTestCase):
    def test_is_installed_command(self):
        debian.is_installed('python')

        self.assertRun('dpkg --status "python" | grep Status')

    def test_install(self):
        debian.install('python')

        self.assertSudo('apt-get -y install "python"', user=RootUser)
