from .Enums import Type

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


class BuiltinCommand:

    def __init__(self, command_str: str):
        self.command_param = " ".join(command_str.split()[1:])
        self.type = Type.BUILTIN

    def operation(self):
        pass


class ExitBuiltinCommand(BuiltinCommand):
    def operation(self):
        return True, None

class EchoBuiltinCommand(BuiltinCommand):
    def operation(self):
        print_words = self.command_param
        print(print_words)
        return False, None

class TypeBuiltinCommand(BuiltinCommand):
    def operation(self):
        command = builtin_factory(self.command_param)
        if command is None:
            print(f"{self.command_param.split(maxsplit=1)[0]}: not found")
        elif command.type == Type.BUILTIN:
            print(f"{self.command_param.split(maxsplit=1)[0]} is a shell builtin")

        return False, None
