from hwt.interfaces.std import Clk, Rst_n, Rst
from hwt.code import connect


def addClkRstn(self):
    self.clk = Clk()
    self.rst_n = Rst_n()


def addClkRst(self):
    self.clk = Clk()
    self.rst = Rst()


def _tryConnect(src, unit, intfName):
    "try connect src to interface of specified name on unit"
    try:
        dst = getattr(unit, intfName)
    except AttributeError:
            dst = None
    if dst is not None:
        connect(src, dst)


def propagateClk(self):
    """
    Propagate "clk" clock signal to all subcomponents
    """
    clk = self.clk
    for u in self._units:
        _tryConnect(clk, u, 'clk')


def propagateClkRstn(self):
    """
    Propagate "clk" clock and negative reset "rst_n" signal to all subcomponents
    """
    clk = self.clk
    rst_n = self.rst_n

    for u in self._units:
        _tryConnect(clk, u, 'clk')
        _tryConnect(rst_n, u, 'rst_n')
        _tryConnect(~rst_n, u, 'rst')


def propagateClkRst(self):
    """
    Propagate "clk" clock and reset "rst" signal to all subcomponents
    """
    clk = self.clk
    rst = self.rst

    for u in self._units:
        _tryConnect(clk, u, 'clk')
        _tryConnect(~rst, u, 'rst_n')
        _tryConnect(rst, u, 'rst')