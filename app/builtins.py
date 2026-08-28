from .Enums import Type
from .executable import executable_factory, Command

def builtin_factory(command: str):
    command_type = command.split(maxsplit=1)[0]
    match command_type:
        case "exit":
            return ExitBuiltinCommand(command)
        case "echo":
            return EchoBuiltinCommand(command)
        case "type":
            return TypeBuiltinCommand(command)
        case _:
            return None


class BuiltinCommand(Command):

    def __init__(self, command_str: str):
        super().__init__(command_str)
        self.type = Type.BUILTIN

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
        elif command.type == Type.BUILTIN:
            print(f"{self.command_param.split(maxsplit=1)[0]} is a shell builtin")

        return False, None
