from amino import Right, List, __, Map, Left
from amino.test.spec_spec import later

from ribosome.test.integration.spec_spec import VimIntegrationSureHelpers

from integration._support.facade import FacadeTestPlugin
from integration._support.base import IntegrationSpecBase


class VimSpec(IntegrationSpecBase, VimIntegrationSureHelpers):

    @property
    def _prefix(self):
        return 'ribosome'

    @property
    def plugin_class(self):
        return Right(FacadeTestPlugin)

    def _last_output(self, content):
        later(lambda: self._log_out.last.should.contain(content), timeout=1)

    def vars(self):
        vname = List.random_string()
        content = [List.random_string()]
        self.vim.cmd_sync('Go')
        self.vim.buffer.vars.set_p(vname, content)
        later(lambda: self.vim.buffer.vars.pl(vname).should.contain(content))
        var = (
            self.vim.call('AllVars') /
            Map //
            __.get('b:{}_{}'.format(self._prefix, vname))
        )
        var.should.contain(str(content))
        self.vim.vars.p(vname).should.be.a(Left)

__all__ = ('VimSpec',)
