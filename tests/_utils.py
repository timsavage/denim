import unittest
from denim.utils import set_api_wrapper, api_wrapper


class Result(object):
    def __init__(self, succeeded=True, return_code=0):
        self.succeeded = succeeded
        self.return_code = return_code


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
        self.commands = []

    def sudo(self, command, **kwargs):
        self.commands.append(('sudo', command, kwargs))
        return Result()

    def run(self, command, **kwargs):
        self.commands.append(('run', command, kwargs))
        return Result()

    def local(self, command, **kwargs):
        self.commands.append(('local', command, kwargs))
        return Result()

set_api_wrapper(TestApiWrapper())


class ApiTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ApiTestCase, self).__init__(*args, **kwargs)
        self.api = api_wrapper()

    def setUp(self):
        self.api.reset()

    def assertCommand(self, expected_command, actual_command):
        e_scope, e_cmd, e_kwargs = expected_command
        a_scope, a_cmd, a_kwargs = actual_command

        self.assertEqual(e_scope, a_scope,
            msg='Command scope does not match. Expected "%s" got "%s"' % (e_scope, a_scope))
        self.assertEqual(e_cmd, a_cmd,
            msg='Command does not match.\nExpected:\t"%s"\nActual:\t"%s"' % (e_cmd, a_cmd))
        self.assertDictEqual(e_kwargs, a_kwargs,
            msg='Command keyword arguments do not match.\nExpected:\t%s\nActual:\t%s' % (e_kwargs, a_kwargs))

    def assertSingeCommand(self, command, _scope, **kwargs):
        user = kwargs.get('user')
        if user and hasattr(user, 'sudo_identity'):
            kwargs['user'] = user.sudo_identity()
        command_count = len(self.api.commands)
        self.assertEqual(command_count, 1, msg="Expected a single command got %s." % command_count)
        self.assertCommand((_scope, command, kwargs), self.api.commands[0])

    def assertSudo(self, command, **kwargs):
        return self.assertSingeCommand(command, _scope='sudo', **kwargs)

    def assertRun(self, command, **kwargs):
        return self.assertSingeCommand(command, _scope='run', **kwargs)

    def assertLocal(self, command, **kwargs):
        return self.assertSingeCommand(command, _scope='local', **kwargs)
