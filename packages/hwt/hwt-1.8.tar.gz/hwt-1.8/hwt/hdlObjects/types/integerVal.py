from hwt.hdlObjects.value import Value, areValues
from hwt.hdlObjects.types.defs import BOOL, INT, SLICE
from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.operatorDefs import AllOps
from hwt.hdlObjects.types.typeCast import toHVal
from hwt.hdlObjects.types.integer import Integer
from operator import pow, eq

BoolVal = BOOL.getValueCls()
SliceVal = SLICE.getValueCls()


def intOp__val(self, other, resT, evalFn):
    v = evalFn(self.val, other.val)
    vldMask = int(self.vldMask and other.vldMask)
    updateTime = max(self.updateTime, other.updateTime)
    return resT.getValueCls()(v, resT, vldMask, updateTime)


def intOp(self, other, op, resT, evalFn=None):
    if evalFn is None:
        evalFn = op._evalFn

    other = toHVal(other)._convert(INT)
    if areValues(self, other):
        return intOp__val(self, other, resT, evalFn)
    else:
        return Operator.withRes(op, [self, other], resT)


def intAritmeticOp(self, other, op):
    return intOp(self, other, op, INT)


def intCmpOp(self, other, op, evalFn=None):
    return intOp(self, other, op, BOOL, evalFn=evalFn)


class IntegerVal(Value):

    def _isFullVld(self):
        return bool(self.vldMask)

    @classmethod
    def fromPy(cls, val, typeObj):
        """
        :param val: value of python type int or None
        :param typeObj: instance of HdlType
        """
        assert isinstance(typeObj, Integer)
        vld = int(val is not None)
        if not vld:
            val = 0
        else:
            val = int(val)

        return cls(val, typeObj, vld)

    # arithmetic
    def _neg__val(self):
        v = self.clone()
        v.val = -self.val
        return v

    def __neg__(self):
        if isinstance(self, Value):
            return self._neg__val()
        else:
            return Operator.withRes(AllOps.UN_MINUS, [self], INT)

    def __add__(self, other):
        return intAritmeticOp(self, other, AllOps.ADD)

    def __sub__(self, other):
        return intAritmeticOp(self, other, AllOps.SUB)

    def __mul__(self, other):
        return intAritmeticOp(self, other, AllOps.MUL)

    def _pow(self, other):
        return intOp(self, other, AllOps.POW, INT, pow)

    def __floordiv__(self, other):
        return intAritmeticOp(self, other, AllOps.DIV)

    def _downto__val(self, other):
        vldMask = int(self.vldMask and other.vldMask)
        updateTime = max(self.updateTime, other.updateTime)
        return SliceVal((self, other), SLICE, vldMask, updateTime)

    def _downto(self, other):
        other = toHVal(other)._convert(INT)
        if areValues(self, other):
            return self._downto__val(other)
        else:
            return Operator.withRes(AllOps.DOWNTO, [self, other], SLICE)

    # comparisons
    def _eq(self, other):
        return intCmpOp(self, other, AllOps.EQ, eq)

    def __ne__(self, other):
        return intCmpOp(self, other, AllOps.NEQ)

    def __le__(self, other):
        return intCmpOp(self, other, AllOps.LE)

    def __lt__(self, other):
        return intCmpOp(self, other, AllOps.LOWERTHAN)

    def __ge__(self, other):
        return intCmpOp(self, other, AllOps.GE)
