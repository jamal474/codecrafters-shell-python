import os
from .Enums import Type

def executable_factory(command: str):
    command_type = command.split(maxsplit=1)[0]
    path_string = os.env.get("PATH", None)

    if path_string is None:
        return None

    paths = path_string.split(":")
    for path in paths:
        folder_elements = os.listdir(path)
        if command_type in folder_elements and os.access(path + command_type, os.X_OK):
            return ExecutableCommand(command, path + command_type)

    return None
            


class Command:
    def __init__(self, command_str: str):
        self.command_str = command_str
        self.command_param = " ".join(command_str.split()[1:])
        self.type = Type.UNKNOWN

    def operation(self):
        pass

    def __str__(self):
        return self.command_str.split(maxsplit=1)[0]

class ExecutableCommand(Command):

    def __init__(self, command_str: str, path: str):
        super().__init__(command_str)
        self.type = Type.EXECUTABLE
        self.path = path
