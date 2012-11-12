from denim.constants import RootUser
from tests._utils import ApiTestCase
from denim.webserver import apache


class TestWebserverApache(ApiTestCase):
    def test_test_config(self):
        apache.test_config()

        self.assertSudo('/usr/sbin/apache2ctl configtest', user=RootUser)

    def test_start(self):
        apache.start()

        self.assertSudo('/etc/init.d/apache2 start', user=RootUser)

    def test_stop(self):
        apache.stop()

        self.assertSudo('/etc/init.d/apache2 stop', user=RootUser)

    def test_restart(self):
        apache.restart(False)

        self.assertSudo('/etc/init.d/apache2 restart', user=RootUser)

    def test_restart(self):
        apache.restart(False)

        self.assertSudo('/etc/init.d/apache2 restart', user=RootUser)

    def test_reload(self):
        apache.reload(False)

        self.assertSudo('/etc/init.d/apache2 reload', user=RootUser)
