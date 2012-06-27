import unittest
from fabric import api
import denim.paths as target


class PathsTest(unittest.TestCase):
    def setUp(self):
        # Required by Denim
        api.env.project_name = 'test-project'
        api.env.package_name = 'test_project'
        api.env.deploy_env = 'test'

        # For testing
        api.env.real_fabfile = '/home/user/projects/test-project'


    def testJoinPath(self):
        self.assertEqual(
            '/path/to/my/stuff',
            target.join_paths('/path/to/my/stuff')
        )
        self.assertEqual(
            '/path/to/my/stuff',
            target.join_paths('/path/to/my/', 'stuff/')
        )
        self.assertEqual(
            '/path/to/my/stuff',
            target.join_paths('/path/to/my', 'stuff')
        )
        self.assertEqual(
            '/path/to/my/stuff',
            target.join_paths('/path/to/', 'my', 'stuff')
        )
        self.assertEqual(
            '/path/to/my/stuff',
            target.join_paths('/path', 'to', 'my', 'stuff/')
        )
        self.assertEqual(
            'path/to/my/stuff',
            target.join_paths('path', 'to', 'my', 'stuff')
        )
        self.assertEqual(
            'path/to/my/stuff',
            target.join_paths('path', 'to', 'my', '/stuff')
        )

    def testDeployPath(self):
        self.assertEqual(
            '/opt/webapps/test-project',
            target.get_deploy_path()
        )
        self.assertEqual(
            '/opt/webapps/test-project',
            target.get_deploy_path('')
        )
        self.assertEqual(
            '/opt/webapps/test-project/var',
            target.get_deploy_path('var')
        )

        self.assertEqual(
            '/opt/webapps/test-project/var',
            target.get_deploy_path('/var')
        )

        api.env.project_name = '/test-project'
        self.assertEqual(
            '/opt/webapps/test-project',
            target.get_deploy_path()
        )

    def testPackagePath(self):
        self.assertEqual(
            '/opt/webapps/test-project/app/current',
            target.get_package_path()
        )
        self.assertEqual(
            '/opt/webapps/test-project/app/current',
            target.get_package_path('')
        )
        self.assertEqual(
            '/opt/webapps/test-project/app/release-1.2.3.4',
            target.get_package_path('release-1.2.3.4')
        )
        self.assertEqual(
            '/opt/webapps/test-project/app/release-1.2.3.4',
            target.get_package_path('release-1.2.3.4')
        )
        self.assertEqual(
            '/opt/webapps/test-project/app/current/var',
            target.get_package_path(sub_path='var')
        )
        self.assertEqual(
            '/opt/webapps/test-project/app/current',
            target.get_package_path(sub_path='')
        )
        self.assertEqual(
            '/opt/webapps/test-project/app/release-1.2.3.4/var',
            target.get_package_path('release-1.2.3.4', 'var')
        )

        self.assertEqual(
            '/opt/webapps/test-project/app/release-1.2.3.4/var',
            target.get_package_path('release-1.2.3.4', '/var')
        )

        api.env.project_name = '/test-project'
        self.assertEqual(
            '/opt/webapps/test-project/app/current',
            target.get_package_path()
        )

    def testLogPath(self):
        self.assertEqual(
            '/var/log/webapps/test-project/test_project',
            target.get_log_path()
        )
        self.assertEqual(
            '/var/log/webapps/test-project/test_project',
            target.get_log_path()
        )

        self.assertEqual(
            '/var/log/webapps/test-project/test_project',
            target.get_log_path()
        )

        api.env.log_path_template = '/opt/webapps/%(project_name)s/%(package_name)s/var/log'
        self.assertEqual(
            '/opt/webapps/test-project/test_project/var/log',
            target.get_log_path()
        )

    def testLogPathBadProjectName(self):
        """
        The value is correct
        """
        api.env.project_name = '/test-project'
        self.assertEqual(
            '/test-project/test_project',
            target.get_log_path()
        )

    def testWSGISocket(self):
        self.assertEqual(
            '/opt/webapps/test-project/var/wsgi.sock',
            target.get_wsgi_socket()
        )

    def testLocalConfigPaths(self):
        self.assertEqual(
            ('test.conf', 'test-project.conf'),
            target.get_local_config_file_names()
        )
        self.assertEqual(
            ('eek-test.conf', 'eek-test-project.conf'),
            target.get_local_config_file_names('eek')
        )

    def testLocalPath(self):
        self.assertEqual(
            '/home/user/projects/test-project',
            target.get_local_path()
        )

        self.assertEqual(
            '/home/user/projects/test-project/var',
            target.get_local_path('var')
        )


    def testLocalConfigPath(self):
        self.assertEqual(
            '/home/user/projects/test-project/conf/nginx/test.conf',
            target.get_local_config_path('nginx')
        )

        self.assertEqual(
            '/home/user/projects/test-project/conf/nginx/foo-test.conf',
            target.get_local_config_path('nginx', 'foo')
        )
