from hwt.hdlObjects.types.hdlType import HdlType


class Boolean(HdlType):

    def __eq__(self, other):
        return type(self) is type(other)

    def __hash__(self):
        return hash(Boolean)

    @classmethod
    def getConvertor(cls):
        from hwt.hdlObjects.types.booleanConversions import convertBoolean
        return convertBoolean

    def bit_length(self):
        return 1

    def all_mask(self):
        return 1

    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hwt.hdlObjects.types.booleanVal import BooleanVal
            cls._valCls = BooleanVal
            return cls._valCls
