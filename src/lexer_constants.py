from string import digits, ascii_letters
from src.tokens import TokenType

RESERVED_WORDS = {
    'var': TokenType.VAR,
    'function': TokenType.FUNCTION,
    'return': TokenType.RETURN,
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'elif': TokenType.ELIF,
    'while': TokenType.WHILE,
    'print': TokenType.PRINT,
    'include': TokenType.INCLUDE,
    'class': TokenType.CLASS,
    'TRUE': TokenType.BOOL,
    'FALSE': TokenType.BOOL,
    'NULL': TokenType.NULL,
}

SINGLE_TOKENS = {
    '(': TokenType.LEFT_PAREN,
    ')': TokenType.RIGHT_PAREN,
    '{': TokenType.LEFT_CURLY,
    '}': TokenType.RIGHT_CURLY,
    '[': TokenType.LEFT_SQUARE,
    ']': TokenType.RIGHT_SQUARE,
    ',': TokenType.COMMA,
    '.': TokenType.DOT,
    '-': TokenType.MINUS,
    '+': TokenType.PLUS,
    ';': TokenType.SEMICOLON,
    '*': TokenType.ASTERISK,
    '^': TokenType.NOT,
    '\n': TokenType.EOL,
}

DOUBLE_TOKENS = {
    '=': {'match': '=', 'yes': TokenType.EQUALITY, 'no': TokenType.EQUALS},
    '!': {'match': '=', 'yes': TokenType.INEQUALITY, 'no': TokenType.NOT},
    '>': {'match': '=', 'yes': TokenType.GTE, 'no': TokenType.GT},
    '<': {'match': '=', 'yes': TokenType.LTE, 'no': TokenType.LT},
    '&': {'match': '&', 'yes': TokenType.AND, 'no': TokenType.ERROR},
    '|': {'match': '|', 'yes': TokenType.OR, 'no': TokenType.ERROR},
}

DISREGARDED_WHITESPACES = {
    ' ', '\r', '\t'
}

STRING_LITERALS = {
    '"', "'"
}

NUMBER_LITERALS = set(digits)

IDENTIFIER_LITERALS = set(ascii_letters) | {'_'}

END_OF_LINE = '\n'
