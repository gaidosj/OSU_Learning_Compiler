# This is the lexer

import sys
import olc_token


# import getopt

class Lexer:
    def __init__(self):
        self.filename = None

    def readfile(self):
        if len(sys.argv) != 2:
            print("Input error")
            return

        print("You've requested that I lex: ", sys.argv[1])
        self.filename = sys.argv[1]
        print("I've imported the tokens, token INT is", olc_token.INT)
        # print(self.filename)

        with open(self.filename, "r") as input_file:
            input_line = input_file.readline()
            while input_line:
                print(input_line)
                input_line = input_file.readline()


OLL_lexer = Lexer()
OLL_lexer.readfile()
