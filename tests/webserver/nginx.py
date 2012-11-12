from denim.constants import RootUser
from tests._utils import ApiTestCase
from denim.webserver import nginx


class TestWebserverNginx(ApiTestCase):
    def test_test_config(self):
        nginx.test_config()

        self.assertSudo('/usr/sbin/nginx -t', user=RootUser)

    def test_start(self):
        nginx.start()

        self.assertSudo('/etc/init.d/nginx start', user=RootUser)

    def test_stop(self):
        nginx.stop()

        self.assertSudo('/etc/init.d/nginx stop', user=RootUser)

    def test_restart(self):
        nginx.restart(False)

        self.assertSudo('/etc/init.d/nginx restart', user=RootUser)

    def test_restart(self):
        nginx.restart(False)

        self.assertSudo('/etc/init.d/nginx restart', user=RootUser)

    def test_reload(self):
        nginx.reload(False)

        self.assertSudo('/usr/sbin/nginx -s reload', user=RootUser)
