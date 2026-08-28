import os
import subprocess
from .Enums import Type

def executable_factory(command: str):
    command_type = command.split(maxsplit=1)[0]
    path_string = os.getenv("PATH", None)

    if path_string is None:
        return None

    paths = path_string.split(os.pathsep)
    for path in paths:
        try:
            folder_elements = os.listdir(path)
            if command_type in folder_elements and os.access(path + os.path.sep + command_type, os.X_OK):
                return ExecutableCommand(command, path + os.path.sep + command_type)
        except:
            continue

    return None
            


class Command:
    cwd: dict = {"path": os.getcwd()}

    def __init__(self, command_str: str):
        self.command_str = command_str
        self.command_param = " ".join(command_str.split()[1:])
        self.type = Type.UNKNOWN

    def run(self):
        pass

    def __str__(self):
        return self.command_str.split(maxsplit=1)[0]

    @classmethod
    def get_pwd(cls):
        return cls.cwd["path"]

class ExecutableCommand(Command):

    def __init__(self, command_str: str, path: str):
        super().__init__(command_str)
        self.type = Type.EXECUTABLE
        self.path = path

    def run(self):
        subprocess.run(self.command_str.split())
        return False, None
