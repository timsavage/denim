from denim.constants import RootUser
from tests._utils import ApiTestCase
from denim.service import supervisor


class TestServiceSupervisor(ApiTestCase):
    def test_manager_start(self):
        supervisor.manager_start()

        self.assertSudo('/etc/init.d/supervisor start', user=RootUser)

    def test_manager_stop(self):
        supervisor.manager_stop()

        self.assertSudo('/etc/init.d/supervisor stop', user=RootUser)

    def test_manager_restart(self):
        supervisor.manager_restart()

        self.assertSudo('/etc/init.d/supervisor restart', user=RootUser)

    def test_manager_reload(self):
        supervisor.manager_reload()

        self.assertSudo('supervisorctl reload', user=RootUser)

    def test_start_default_service(self):
        supervisor.start()

        self.assertSudo('supervisorctl start test-project', user=RootUser)

    def test_start_custom_service(self):
        supervisor.start('bar')

        self.assertSudo('supervisorctl start bar', user=RootUser)

    def test_stop_default_service(self):
        supervisor.stop()

        self.assertSudo('supervisorctl stop test-project', user=RootUser)

    def test_stop_custom_service(self):
        supervisor.stop('bar')

        self.assertSudo('supervisorctl stop bar', user=RootUser)

    def test_restart_default_service(self):
        supervisor.restart()

        self.assertSudo('supervisorctl restart test-project', user=RootUser)

    def test_restart_custom_service(self):
        supervisor.restart('bar')

        self.assertSudo('supervisorctl restart bar', user=RootUser)

    def test_status_default_service(self):
        supervisor.status()

        self.assertSudo('supervisorctl status test-project', user=RootUser)

    def test_status_custom_service(self):
        supervisor.status('bar')

        self.assertSudo('supervisorctl status bar', user=RootUser)

