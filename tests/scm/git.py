from tests._utils import ApiTestCase
from denim.scm import git


class TestScmGit(ApiTestCase):
    def test_tag(self):
        git.tag('Foo bar', 'foo')

        self.assertLocal('git tag -a -m "Foo bar" foo')

    def test_archive(self):
        git.archive('deploy-2012-04-23', '/tmp/outfile.tar', 'app')

        self.assertLocal('git archive deploy-2012-04-23 app > /tmp/outfile.tar')

    def test_archive_with_prefix(self):
        git.archive('deploy-2012-04-23', '/tmp/outfile.tar', 'app', prefix='bar')

        self.assertLocal('git archive --prefix=bar deploy-2012-04-23 app > /tmp/outfile.tar')

    def test_export_file(self):
        git.export_file('deploy-2012-04-23', 'requirements.txt', '/tmp/requirements.txt')

        self.assertLocal('git show deploy-2012-04-23:requirements.txt > /tmp/requirements.txt')

    def test_get_hash(self):
        git.get_hash('deploy-2012-04-23')

        self.assertLocal('git log -1 --pretty=format:\'%H\' deploy-2012-04-23', capture=True)

    def test_get_revision_name(self):
        result = git.get_revision_name('deploy-2012-04-23')

        self.assertEqual(result, 'deploy-2012-04-23')

    def test_get_revision_revision_is_master(self):
        git.get_revision_name('master')

        self.assertLocal('git log -1 --pretty=format:\'%H\' master', capture=True)