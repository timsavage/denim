import unittest
from denim.utils import set_api_wrapper, api_wrapper


class TestApiWrapper(object):
    """
    An easily replaceable wrapper around api commands to allow for easy
    testing.
    """
    def __init__(self):
        self.reset()

    def reset(self):
        """
        Clear all commands.
        """
        self.sudo_commands = []
        self.run_commands = []

    def sudo(self, command, *args, **kwargs):
        return self.sudo_commands.append((command, args, kwargs))

    def run(self, command, *args, **kwargs):
        return self.run_commands.append((command, args, kwargs))

set_api_wrapper(TestApiWrapper())


class ApiTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ApiTestCase, self).__init__(*args, **kwargs)
        self.api = api_wrapper()

    def setUp(self):
        self.api.reset()

    def assertCommand(self, expected_command, actual_command):
        ec, ea, ekwa = expected_command
        ac, aa, akwa = actual_command

        self.assertEqual(ec, ac, msg='Command does not match. Expected "%s" got "%s"' % (ec, ac))
        self.assertTupleEqual(ea, aa, msg='Command arguments do not match.\nExpected: %s\nActual: %s' % (ea, aa))
        self.assertDictEqual(ekwa, akwa, msg='Command keyword arguments do not match.\nExpected: %s\nActual: %s' % (ekwa, akwa))

    def assertSudo(self, command, *args, **kwargs):
        command_count = len(self.api.sudo_commands)
        self.assertEqual(command_count, 1, msg="Expected a single sudo command got %s." % command_count)
        self.assertCommand((command, args, kwargs), self.api.sudo_commands[0])

    def assertRun(self, command, *args, **kwargs):
        command_count = len(self.api.run_commands)
        self.assertEqual(command_count, 1, msg="Expected a single run command got %s." % command_count)
        self.assertCommand((command, args, kwargs), self.api.run_commands[0])
