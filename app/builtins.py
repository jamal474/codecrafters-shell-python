def builtin_factory(command: str):
    command_type = command.split(" ")[0]
    match command_type:
        case "exit":
            return ExitBuiltinCommand(command)
        case "echo":
            return EchoBuiltinCommand(command)
        case _:
            return None


class BuiltinCommand:

    def __init__(self, command_str: str):
        self.command = command_str

    def operation(self):
        pass


class ExitBuiltinCommand(BuiltinCommand):
    def operation(self):
        return True, None

class EchoBuiltinCommand(BuiltinCommand):
    def operation(self):
        print_words = self.command.split(" ")[1:]
        print(" ".join(print_words))
        return False, None
