import sys, os
from .builtins import builtin_factory
from .executable import executable_factory, Command

def _command_resolver(command_string: str):
    command_obj = builtin_factory(command_string)
    if command_obj is None:
        command_obj = executable_factory(command_string)
    return command_obj


def main():

    while True:
        if os.path.exists(Command.get_pwd()):
            os.chdir(Command.get_pwd())
        
        sys.stdout.write("$ ")
        user_input = input()
        command_handler = _command_resolver(user_input)

        if command_handler == None:
            print(f"{user_input.split(" ")[0]}: command not found")
            continue

        exit, output = command_handler.run()

        if exit:
            break
    pass


if __name__ == "__main__":
    main()
