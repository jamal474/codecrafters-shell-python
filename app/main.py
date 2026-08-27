import sys
from .builtins import builtin_factory

def _command_resolver(command_string: str):
    return builtin_factory(command_string)


def main():

    while True:
        sys.stdout.write("$ ")
        user_input = input()
        command_handler = _command_resolver(user_input)

        if command_handler == None:
            print(f"{user_input.split(" ")[0]}: command not found")
            continue

        exit, output = command_handler.operation()

        if exit:
            break
    pass


if __name__ == "__main__":
    main()
