import os
import logging
from .types import CommandType
from .constants import CURRENT_DIR_PREFIX, PARENT_DIR_PREFIX
from .executable import executable_factory, Command

logger = logging.getLogger(__name__)

def builtin_factory(command: str):
    command_type = command.split(maxsplit=1)[0]
    match command_type:
        case "exit":
            return ExitBuiltinCommand(command)
        case "echo":
            return EchoBuiltinCommand(command)
        case "type":
            return TypeBuiltinCommand(command)
        case "pwd":
            return PwdBuiltinCommand(command)
        case "cd":
            return CdBuiltinCommand(command)
        case _:
            return None


class BuiltinCommand(Command):

    def __init__(self, command_str: str):
        super().__init__(command_str)
        self.type = CommandType.BUILTIN

    def run(self):
        pass


class ExitBuiltinCommand(BuiltinCommand):
    def run(self):
        return True, None

class EchoBuiltinCommand(BuiltinCommand):
    def run(self):
        print_words = self.command_param
        print(print_words)
        return False, None

class TypeBuiltinCommand(BuiltinCommand):
    def run(self):
        command = builtin_factory(self.command_param)
        if command is None:
            # Could be a executable
            command = executable_factory(self.command_param)
            if command is not None:
                print(f"{command} is {command.path}")
            else:
                print(f"{self.command_param.split(maxsplit=1)[0]}: not found")
        elif command.type == CommandType.BUILTIN:
            print(f"{self.command_param.split(maxsplit=1)[0]} is a shell builtin")

        return False, None

class PwdBuiltinCommand(BuiltinCommand):
    def run(self):
        print(os.getcwd())
        return False, None

class CdBuiltinCommand(BuiltinCommand):

    def _abs_path_handler(self, path_string: str):
        """
        Absolute Path Handler: of the form,
        - /path... : starting with [ **/** ]

        Parameters:
            path_string (str): Path of the file/folder
        Returns:
            bool: signifying wether path is absolute or not
        """
        if os.path.isabs(path_string):
            if os.path.exists(path_string):
                self.set_cwd(path_string)

            return True
        return False
    
    def _resolve_parent_stack(self, parent_str: str):
        logger.info("Resolve Parent Stack Command")
        prefix, rest_str = parent_str.split("/",maxsplit=1)
        parent_wd = self.get_cwd()
        folder_path_after_parent = ""
        while prefix == PARENT_DIR_PREFIX:
            logger.info(f"prefix:{prefix} , other part: {rest_str}")
            parent_wd = os.path.dirname(parent_wd)
            logger.info(f"resolved parent string: {parent_wd}")
            try:
                prefix, rest_str = rest_str.split("/", maxsplit=1)
            except Exception:
                logger.info(f"Could not extract parent command, exiting loop with Folder as {rest_str}")
                folder_path_after_parent = rest_str
                break
        return parent_wd, folder_path_after_parent

    def _relative_path_handler(self, path_string: str):
        """
        Relative Path Handler: path_string could be one
        of the following
        - ./path : relative to current working directory (cwd)
        - ../path : relative to parent of cwd
        - path : relative to cwd, similar to ./path
        """
        if path_string == "" or path_string == None:
            return False

        try:
            type_prefix, rest_str = path_string.split("/", maxsplit=1)
        except Exception as e:
            logger.info("path does not have enough separator to split")
            type_prefix = path_string.split("/", maxsplit=1)[0]

        if type_prefix == CURRENT_DIR_PREFIX:
            logger.info(f"Type Prefix: Current Directory {type_prefix}")
            absolute_path = os.path.join(self.get_cwd(), rest_str)
            logger.info(f"Absolute path : {absolute_path}")
            if os.path.exists(absolute_path):
                self.set_cwd(absolute_path)
            return True
        elif type_prefix == PARENT_DIR_PREFIX:
            logger.info(f"Type Prefix: Parent Directory {type_prefix}")
            parent_wd, rest_str = self._resolve_parent_stack(path_string)
            absolute_path = os.path.join(parent_wd, rest_str)
            logger.info(f"Absolute path : {absolute_path}")
            if os.path.exists(absolute_path):
                self.set_cwd(absolute_path)
            return True
        else:
            logger.info(f"Type Prefix: Not Among ./ or ../ {type_prefix}")
            absolute_path = os.path.join(self.get_cwd(), path_string)
            if os.path.exists(absolute_path):
                self.set_cwd(absolute_path)
                return True
        return False
    
    def run(self):
        path_string = self.command_param
        path_exists = ( self._abs_path_handler(path_string) or 
                       self._relative_path_handler(path_string))
        if not path_exists:
            print(f"cd: {self.command_param}: No such file or directory")
        
        return False, None
