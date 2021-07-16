# This is the orchestrator

import sys
import olc_token


# import getopt

class Olc:
    def __init__(self):
        self.filename = None

    def readfile(self):
        if len(sys.argv) != 2:
            print("Input error")
            return

        print("You've requested that I lex: ", sys.argv[1])
        self.filename = sys.argv[1]
        # print(self.filename)

        with open(self.filename, "r") as input_file:
            input_line = input_file.readline()
            while input_line:
                print(input_line)
                input_line = input_file.readline()


OLL = Olc()
OLL.readfile()
