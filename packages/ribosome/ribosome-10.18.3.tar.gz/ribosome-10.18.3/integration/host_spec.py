from kallikrein import k, Expectation

from amino.test.path import fixture_path
from amino import Either, Right

from ribosome.test.integration.spec import PluginIntegrationSpec
from ribosome.rpc import define_handlers, rpc_handlers

from integration._support.plugin import TestPluginUnlooped


class HostSpec(PluginIntegrationSpec):
    '''
    test $test
    '''

    @property
    def _prefix(self) -> str:
        return 'host'

    @property
    def autostart_plugin(self) -> bool:
        return False

    @property
    def plugin_class(self) -> Either[str, type]:
        return Right(TestPluginUnlooped)

    def test(self) -> Expectation:
        exe = fixture_path('host', 'run')
        plug = self.rplugin_path.get_or_raise
        channel = self.vim.call('jobstart', ['/home/tek/usr/opt/pyenv/shims/python', str(exe), str(plug)],
                                dict(rpc=True)).get_or_raise
        handlers = rpc_handlers(self.plugin_class.get_or_raise)
        define_handlers(channel, handlers, 'host', str(plug)).attempt(self.vim).get_or_raise
        self._wait(1)
        self.cmd_sync('Go')
        self.cmd_sync('TstUv')
        self._wait(1)
        return k(1) == 1

__all__ = ('HostSpec',)
