from tests._utils import ApiTestCase
from denim.scm import hg


class TestScmHG(ApiTestCase):
    def test_tag(self):
        hg.tag('Foo bar', 'foo')

        self.assertLocal('hg tag -m "Foo bar" foo')

    def test_archive(self):
        hg.archive('deploy-2012-04-23', '/tmp/outfile.tar', 'app')

        self.assertLocal('hg archive -r deploy-2012-04-23 -I app /tmp/outfile.tar')

    def test_archive_with_prefix(self):
        hg.archive('deploy-2012-04-23', '/tmp/outfile.tar', 'app', prefix='bar')

        self.assertLocal('hg archive -r deploy-2012-04-23 -I app -p bar /tmp/outfile.tar')

    def test_export_file(self):
        hg.export_file('deploy-2012-04-23', 'requirements.txt', '/tmp/requirements.txt')

        self.assertLocal('hg cat -r deploy-2012-04-23 requirements.txt > /tmp/requirements.txt')

    def test_get_hash(self):
        hg.get_hash('deploy-2012-04-23')

        self.assertLocal('hg id -i -r deploy-2012-04-23', capture=True)

    def test_get_revision_name(self):
        result = hg.get_revision_name('deploy-2012-04-23')

        self.assertEqual(result, 'deploy-2012-04-23')

    def test_get_revision_revision_is_default(self):
        hg.get_revision_name('default')

        self.assertLocal('hg id -i -r default', capture=True)
