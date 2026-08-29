from enum import Enum

class Type(Enum):
    pass

class CommandType(Type):
    BUILTIN = 1
    EXECUTABLE = 2
    UNKNOWN = 3