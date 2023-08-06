from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.operatorDefs import AllOps
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.booleanVal import BooleanVal
from hwt.hdlObjects.types.defs import BOOL
from hwt.hdlObjects.types.hdlType import HdlType
from hwt.hdlObjects.value import Value


def convertInteger(self, sigOrVal, toType):
    isVal = isinstance(sigOrVal, Value)
    if toType == BOOL:
        if isVal:
            v = sigOrVal.val
            assert v == 0 or v == 1
            return BooleanVal(v, BOOL, sigOrVal.vldMask, sigOrVal.updateTime)

    elif isinstance(toType, Bits):
        if isVal:
            _v = sigOrVal.val
            w = toType.bit_length()
            assert _v.bit_length() <= w, "%d can not fit into %d bits" % (_v, w)
            v = toType.fromPy(_v)

            v.updateTime = sigOrVal.updateTime

            v._dtype = toType
            if not sigOrVal.vldMask:
                v.vldMask = 0
            return v
        else:
            return Operator.withRes(AllOps.IntToBits, [sigOrVal], toType)

    return HdlType.defaultConvert(self, sigOrVal, toType)
