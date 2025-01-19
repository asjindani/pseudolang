import sys
import os.path
from .modules.program import Program

def run():
    arguments = sys.argv.copy()

    DEV = "-dev"
    dev_flag = False
    if DEV in arguments:
        dev_flag = True
    while DEV in arguments:
        arguments.remove(DEV)

    if len(arguments) > 1:
        file_path = arguments[1]
    else:
        file_path = input("Enter file path: ")

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            lines = [line.strip() for line in file.readlines()]

        program = Program(lines, dev=dev_flag)
        program.parse()
        program.run()
    else:
        print(f"File '{file_path}' not found")

if __name__ == "__main__":
    run()