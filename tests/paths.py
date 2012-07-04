import unittest
import os
from fabric import api
import denim.paths as target


class PathTestCaseBase(unittest.TestCase):
    def setUp(self):
        # Required by Denim
        api.env.project_name = 'test-project'
        api.env.package_name = 'test_project'
        api.env.deploy_env = 'test'

        # Required for test cases
        api.env.real_fabfile = __file__

    def make_local_path(self, *args):
        """ Helper function for testing OS specific local paths """
        return os.path.normpath(os.path.join(
            os.path.dirname(api.env.real_fabfile), *args).rstrip(os.path.sep))


class JoinPathsTestCase(PathTestCaseBase):
    def testSinglePath(self):
        self.assertEqual(
            '/path/to/my/stuff',
            target.join_paths('/path/to/my/stuff')
        )

    def testMultiplePaths(self):
        self.assertEqual(
            '/path/to/my/stuff',
            target.join_paths('/path/to/', 'my', 'stuff')
        )

    def testMultiplePathsWithEndSeparator(self):
        self.assertEqual(
            '/path/to/my/stuff',
            target.join_paths('/path', 'to', 'my', 'stuff/')
        )

    def testRelativePath(self):
        self.assertEqual(
            'path/to/my/stuff',
            target.join_paths('path', 'to', 'my', 'stuff')
        )

    def testSeparatorMidPath(self):
        self.assertEqual(
            'path/to/my/stuff',
            target.join_paths('path', 'to', 'my', '/stuff')
        )


class DeployPathTestCase(PathTestCaseBase):
    def testDefaultPath(self):
        self.assertEqual(
            '/opt/webapps/test-project',
            target.deploy_path()
        )

    def testEmptySubPath(self):
        self.assertEqual(
            '/opt/webapps/test-project',
            target.deploy_path('')
        )

    def testSubPath(self):
        self.assertEqual(
            '/opt/webapps/test-project/var',
            target.deploy_path('var')
        )


class PackagePathTestCase(PathTestCaseBase):
    def testDefaultPath(self):
        self.assertEqual(
            '/opt/webapps/test-project/app/current',
            target.package_path()
        )

    def testEmptyReleaseName(self):
        self.assertEqual(
            '/opt/webapps/test-project/app/current',
            target.package_path('')
        )

    def testWithRelease(self):
        self.assertEqual(
            '/opt/webapps/test-project/app/release-1.2.3.4',
            target.package_path('release-1.2.3.4')
        )

    def testWithEmptySubPath(self):
        self.assertEqual(
            '/opt/webapps/test-project/app/release-1.2.3.4',
            target.package_path('release-1.2.3.4', '')
        )

    def testWithEmptyReleaseAndSubPath(self):
        self.assertEqual(
            '/opt/webapps/test-project/app/current',
            target.package_path('', '')
        )

    def testWithSubPath(self):
        self.assertEqual(
            '/opt/webapps/test-project/app/current/var',
            target.package_path(sub_path='var')
        )


class OtherDeployPathsTestCase(PathTestCaseBase):
    def testLogPath(self):
        self.assertEqual(
            '/var/log/webapps/test-project/test_project',
            target.log_path()
        )

    def testWSGISocket(self):
        self.assertEqual(
            '/opt/webapps/test-project/var/wsgi.sock',
            target.wsgi_socket_path()
        )


class RemoteConfigFileTestCase(PathTestCaseBase):
    def testDefaultPath(self):
        self.assertEqual(
            '/etc/nginx/sites-available/test-project.conf',
            target.remote_config_file('/etc/nginx/sites-available')
        )

    def testWithNamePrefix(self):
        self.assertEqual(
            '/etc/nginx/sites-available/test-test-project.conf',
            target.remote_config_file('/etc/nginx/sites-available', 'test')
        )

    def testWithAlternateExtension(self):
        self.assertEqual(
            '/etc/nginx/sites-available/test-project.rc',
            target.remote_config_file('/etc/nginx/sites-available', extension='.rc')
        )


if os.name == 'nt':
    class JoinLocalPathsTestCase(PathTestCaseBase):
        def testSinglePath(self):
            self.assertEqual(
                r'C:\path\to\my\stuff',
                target.join_local_paths(r'C:\path\to\my\stuff')
            )

        def testMultiplePaths(self):
            self.assertEqual(
                r'C:\path\to\my\stuff',
                target.join_local_paths('C:\\path\\to\\', 'my', 'stuff')
            )

        def testMultiplePathsWithEndSeparator(self):
            self.assertEqual(
                r'C:\path\to\my\stuff',
                target.join_local_paths('C:\\path', 'to', 'my', 'stuff\\')
            )

        def testRelativePath(self):
            self.assertEqual(
                r'path\to\my\stuff',
                target.join_local_paths('path', 'to', 'my', 'stuff')
            )

        def testSeparatorMidPath(self):
            self.assertEqual(
                r'path\to\my\stuff',
                target.join_local_paths('path', 'to', 'my', '\\stuff')
            )
else:
    class JoinLocalPathsTestCase(PathTestCaseBase):
        def testSinglePath(self):
            self.assertEqual(
                '/path/to/my/stuff',
                target.join_local_paths('/path/to/my/stuff')
            )

        def testMultiplePaths(self):
            self.assertEqual(
                '/path/to/my/stuff',
                target.join_local_paths('/path/to/', 'my', 'stuff')
            )

        def testMultiplePathsWithEndSeparator(self):
            self.assertEqual(
                '/path/to/my/stuff',
                target.join_local_paths('/path', 'to', 'my', 'stuff/')
            )

        def testRelativePath(self):
            self.assertEqual(
                'path/to/my/stuff',
                target.join_local_paths('path', 'to', 'my', 'stuff')
            )

        def testSeparatorMidPath(self):
            self.assertEqual(
                'path/to/my/stuff',
                target.join_local_paths('path', 'to', 'my', '/stuff')
            )


class LocalPathTestCase(PathTestCaseBase):
    def testDefaultPath(self):
        self.assertEqual(
            self.make_local_path(),
            target.local_path()
        )

    def testEmptySubPath(self):
        self.assertEqual(
            self.make_local_path(),
            target.local_path('')
        )

    def testSubPath(self):
        self.assertEqual(
            self.make_local_path('var'),
            target.local_path('var')
        )


class LocalConfigFileOptionsTestCase(PathTestCaseBase):
    def testDefaultPath(self):
        self.assertEqual(
            [
                self.make_local_path('conf/nginx/test.conf'),
                self.make_local_path('conf/nginx.conf'),
            ],
            target.local_config_file_options('nginx')
        )

    def testWithNamePrefix(self):
        self.assertEqual(
            [
                self.make_local_path('conf/nginx/alt-test.conf'),
                self.make_local_path('conf/nginx/test.conf'),
                self.make_local_path('conf/alt-nginx.conf'),
                self.make_local_path('conf/nginx.conf'),
            ],
            target.local_config_file_options('nginx', 'alt')
        )

    def testWithAlternateExtension(self):
        self.assertEqual(
            [
                self.make_local_path('conf/nginx/test.rc'),
                self.make_local_path('conf/nginx.rc'),
            ],
            target.local_config_file_options('nginx', extension='.rc')
        )


class LocalConfigFileTestCase(PathTestCaseBase):
    def testDefaultPath(self):
        self.assertEqual(
            self.make_local_path('conf/nginx.conf'),
            target.local_config_file('nginx')
        )

    def testWithNamePrefix(self):
        self.assertEqual(
            self.make_local_path('conf/nginx/alt-test.conf'),
            target.local_config_file('nginx', 'alt')
        )

    def testWithAlternateExtension(self):
        self.assertEqual(
            self.make_local_path('conf/nginx/test.rc'),
            target.local_config_file('nginx', extension='.rc')
        )
