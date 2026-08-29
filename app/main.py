import sys, os
import logging
from dotenv import load_dotenv
from .builtins import builtin_factory
from .executable import executable_factory, Command

load_dotenv()

logging.basicConfig(
    level=os.getenv("LEVEL"),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

def _command_resolver(command_string: str):
    command_obj = builtin_factory(command_string)
    if command_obj is None:
        command_obj = executable_factory(command_string)
    return command_obj


def main():

    def _resolve_cwd():
        _cwd = Command.get_cwd()
        if os.path.exists(_cwd):
            logger.info(f"Changing Current Working Directory to {_cwd}")
            os.chdir(_cwd)

    while True:
        _resolve_cwd()
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
    logger.info(f"Application Started: ENV {os.getenv("LEVEL")}")
    main()
