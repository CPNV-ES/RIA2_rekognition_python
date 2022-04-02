

from enum import Enum


class AttributeType(Enum):
    STRING = 0
    NUMBER = 1
    BOOLEAN = 2
    NONE = -1

    @classmethod
    def type(cls, value):
        if (value is str):
            return AttributeType.STRING
        elif (value is float or value is int):
            return AttributeType.NUMBER
        elif (value is bool):
            return AttributeType.BOOLEAN
        else:
            return AttributeType.NONE
