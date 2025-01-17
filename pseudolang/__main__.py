import sys
import os.path
from .program import Program

if __name__ == "__main__":
    file_path = sys.argv[1]

    dev_flag = False
    if "-dev" in sys.argv:
        dev_flag = True

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            lines = [line.strip() for line in file.readlines()]

        program = Program(lines, dev=dev_flag)
        program.parse()
        program.run()
    else:
        print("File not found")

del os.path
del sys