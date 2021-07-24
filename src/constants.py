from enum import Enum


class Color:
    BrightBlack = '\u001b[30;1m'
    BrightRed = '\u001b[31;1m'
    BrightGreen = '\u001b[32;1m'
    BrightYellow = '\u001b[33;1m'
    BrightBlue = '\u001b[34;1m'
    BrightMagenta = '\u001b[35;1m'
    BrightCyan = '\u001b[36;1m'
    BrightWhite = '\u001b[37;1m'
    Reset = '\u001b[0m'


class AppType(Enum):
    AST = 'Abstract Syntax Tree class for storing / printing the AST'
    PARSER = 'Parser class'
    INTERPRETER = 'Interpreter class'
    ENVIRONMENT = 'Storage for variable name - value bindings'
