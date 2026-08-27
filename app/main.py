import sys


def main():

    while True:
        sys.stdout.write("$ ")
        command = input()

        if command is "exit":
            break
        
        print(f"{command}: command not found")
    pass


if __name__ == "__main__":
    main()
