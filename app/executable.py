import os
import subprocess
import logging
from .types import CommandType

logger = logging.getLogger(__name__)

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
        self.type = CommandType.UNKNOWN

    def run(self):
        pass

    def __str__(self):
        return self.command_str.split(maxsplit=1)[0]

    @classmethod
    def get_cwd(cls):
        logger.info(f"[GET] Current Working Directory: {cls.cwd["path"]}")
        return cls.cwd["path"]

    @classmethod
    def set_cwd(cls, path_str: str):
        logger.info(f"[SET] Current Working Directory: {path_str}")
        cls.cwd["path"] = path_str

class ExecutableCommand(Command):

    def __init__(self, command_str: str, path: str):
        super().__init__(command_str)
        self.type = CommandType.EXECUTABLE
        self.path = path

    def run(self):
        subprocess.run(self.command_str.split())
        return False, None
