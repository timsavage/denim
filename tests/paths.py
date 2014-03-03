# -*- encoding:utf8 -*-
import unittest
import os

from fabric import api

import denim.paths as target


class PathTestCaseBase(unittest.TestCase):
    def setUp(self):
        # Required for test cases
        api.env.real_fabfile = __file__

    def make_local_path(self, *args):
        """ Helper function for testing OS specific local paths """
        return os.path.normpath(os.path.join(
            os.path.dirname(api.env.real_fabfile), *args).rstrip(os.path.sep))


class JoinPathsTestCase(PathTestCaseBase):
    def test_SinglePath(self):
        self.assertEqual(
            '/path/to/my/stuff',
            target.join_paths('/path/to/my/stuff')
        )

    def test_MultiplePaths(self):
        self.assertEqual(
            '/path/to/my/stuff',
            target.join_paths('/path/to/', 'my', 'stuff')
        )

    def test_MultiplePathsWithEndSeparator(self):
        self.assertEqual(
            '/path/to/my/stuff',
            target.join_paths('/path', 'to', 'my', 'stuff/')
        )

    def test_RelativePath(self):
        self.assertEqual(
            'path/to/my/stuff',
            target.join_paths('path', 'to', 'my', 'stuff')
        )

    def test_SeparatorMidPath(self):
        self.assertEqual(
            'path/to/my/stuff',
            target.join_paths('path', 'to', 'my', '/stuff')
        )


class ProjectPathTestCase(PathTestCaseBase):
    def test_DefaultPath(self):
        self.assertEqual(
            '/opt/test-project',
            target.project_path()
        )

    def test_EmptySubPath(self):
        self.assertEqual(
            '/opt/test-project',
            target.project_path('')
        )

    def test_SubPath(self):
        self.assertEqual(
            '/opt/test-project/var',
            target.project_path('var')
        )


class ReleasePathTestCase(PathTestCaseBase):
    def test_DefaultPath(self):
        self.assertEqual(
            '/opt/test-project/current',
            target.release_path()
        )

    def test_EmptyReleaseName(self):
        self.assertEqual(
            '/opt/test-project/current',
            target.release_path('')
        )

    def test_WithRelease(self):
        self.assertEqual(
            '/opt/test-project/releases/release-1.2.3.4',
            target.release_path('release-1.2.3.4')
        )

    def test_WithEmptySubPath(self):
        self.assertEqual(
            '/opt/test-project/releases/release-1.2.3.4',
            target.release_path('release-1.2.3.4', '')
        )

    def test_WithEmptyReleaseAndSubPath(self):
        self.assertEqual(
            '/opt/test-project/current',
            target.release_path('', '')
        )

    def test_WithSubPath(self):
        self.assertEqual(
            '/opt/test-project/current/var',
            target.release_path(sub_path='var')
        )


class OtherDeployPathsTestCase(PathTestCaseBase):
    def test_LogPath(self):
        self.assertEqual(
            '/var/log/test-project',
            target.log_path()
        )

    def test_WSGISocket(self):
        self.assertEqual(
            '/opt/test-project/var/wsgi.sock',
            target.wsgi_socket_path()
        )


class RemoteConfigFileTestCase(PathTestCaseBase):
    def test_DefaultPath(self):
        self.assertEqual(
            '/etc/nginx/sites-available/test-project.conf',
            target.remote_config_file('/etc/nginx/sites-available')
        )

    def test_WithNamePrefix(self):
        self.assertEqual(
            '/etc/nginx/sites-available/test-test-project.conf',
            target.remote_config_file('/etc/nginx/sites-available', 'test')
        )

    def test_WithAlternateExtension(self):
        self.assertEqual(
            '/etc/nginx/sites-available/test-project.rc',
            target.remote_config_file('/etc/nginx/sites-available', extension='.rc')
        )


if os.name == 'nt':
    class JoinLocalPathsTestCase(PathTestCaseBase):
        def test_SinglePath(self):
            self.assertEqual(
                r'C:\path\to\my\stuff',
                target.join_local_paths(r'C:\path\to\my\stuff')
            )

        def test_MultiplePaths(self):
            self.assertEqual(
                r'C:\path\to\my\stuff',
                target.join_local_paths('C:\\path\\to\\', 'my', 'stuff')
            )

        def test_MultiplePathsWithEndSeparator(self):
            self.assertEqual(
                r'C:\path\to\my\stuff',
                target.join_local_paths('C:\\path', 'to', 'my', 'stuff\\')
            )

        def test_RelativePath(self):
            self.assertEqual(
                r'path\to\my\stuff',
                target.join_local_paths('path', 'to', 'my', 'stuff')
            )

        def test_SeparatorMidPath(self):
            self.assertEqual(
                r'path\to\my\stuff',
                target.join_local_paths('path', 'to', 'my', '\\stuff')
            )
else:
    class JoinLocalPathsTestCase(PathTestCaseBase):
        def test_SinglePath(self):
            self.assertEqual(
                '/path/to/my/stuff',
                target.join_local_paths('/path/to/my/stuff')
            )

        def test_MultiplePaths(self):
            self.assertEqual(
                '/path/to/my/stuff',
                target.join_local_paths('/path/to/', 'my', 'stuff')
            )

        def test_MultiplePathsWithEndSeparator(self):
            self.assertEqual(
                '/path/to/my/stuff',
                target.join_local_paths('/path', 'to', 'my', 'stuff/')
            )

        def test_RelativePath(self):
            self.assertEqual(
                'path/to/my/stuff',
                target.join_local_paths('path', 'to', 'my', 'stuff')
            )

        def test_SeparatorMidPath(self):
            self.assertEqual(
                'path/to/my/stuff',
                target.join_local_paths('path', 'to', 'my', '/stuff')
            )


class LocalPathTestCase(PathTestCaseBase):
    def test_DefaultPath(self):
        self.assertEqual(
            self.make_local_path(),
            target.local_path()
        )

    def test_EmptySubPath(self):
        self.assertEqual(
            self.make_local_path(),
            target.local_path('')
        )

    def test_SubPath(self):
        self.assertEqual(
            self.make_local_path('var'),
            target.local_path('var')
        )


class LocalWorkingPathTestCase(PathTestCaseBase):
    def setUp(self):
        # Clean up test folder as this test creates stuff.
        try:
            os.removedirs(self.make_local_path('den/foo'))
        except OSError:
            pass

    def test_DefaultPath(self):
        expected = self.make_local_path('den')
        self.assertEqual(
            expected,
            target.local_working_path()
        )
        self.assertTrue(os.path.exists(expected))

    def test_SubPath(self):
        expected = self.make_local_path('den/foo')
        self.assertEqual(
            expected,
            target.local_working_path('foo')
        )
        self.assertTrue(os.path.exists(expected))

    def test_NoCreate(self):
        expected = self.make_local_path('den/foo')
        self.assertEqual(
            expected,
            target.local_working_path('foo', ensure_exists=False)
        )
        self.assertFalse(os.path.exists(expected))

    def test_WithFilename(self):
        expected = self.make_local_path('den/bar.txt')
        self.assertEqual(
            expected,
            target.local_working_path(file_name='bar.txt')
        )


class LocalConfigFileTestCase(PathTestCaseBase):
    def test_DefaultPath(self):
        self.assertEqual(
            self.make_local_path('conf/nginx.conf'),
            target.local_config_file('nginx')
        )

    def test_WithNamePrefix(self):
        self.assertEqual(
            self.make_local_path('conf/nginx/alt-test.conf'),
            target.local_config_file('nginx', 'alt')
        )

    def test_WithAlternateExtension(self):
        self.assertEqual(
            self.make_local_path('conf/nginx/test.rc'),
            target.local_config_file('nginx', extension='.rc')
        )

    def test_NotFound(self):
        self.assertIsNone(
            target.local_config_file('supervisor', abort_if_not_found=False)
        )

    def test_AbortIfNotFound(self):
        self.assertRaises(SystemExit,
            lambda: target.local_config_file('supervisor'))
