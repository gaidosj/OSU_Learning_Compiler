from enum import Enum


class Token:
    def __init__(self, token_type, lexeme, literal, source_file_line_number=0):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.source_file_line_number = source_file_line_number

    def __str__(self):
        return '{} {} {}'.format(self.type, self.lexeme, self.literal)

    def __repr__(self):
        return '{} {} {}'.format(self.type, self.lexeme, self.literal)


class DataType(Enum):
    INT = 'int'
    FLOAT = 'float'
    STRING = 'string'
    BOOL = 'bool'
    OBJECT = 'object'


class TokenType(Enum):

    # Math operators
    EQUALS = '='            # double with EQUALITY
    PLUS = '+'              # single
    MINUS = '-'             # single
    ASTERISK = '*'          # single
    DIV = '/'               # double with COMMENT

    # Logic operators
    LT = '<'                # double with LTE
    LTE = '<='              # double with LT
    GT = '>'                # double with GTE
    GTE = '>='              # double with GT
    EQUALITY = '=='         # double with EQUALS
    INEQUALITY = '!='       # double with NOT

    # boolean operations
    NOT = '!'               # double with INEQUALITY
    AND = '&&'              # double with ERROR
    OR = '||'               # double with ERROR
    XOR = '^'               # single

    # Bracket types
    LEFT_PAREN = '('        # single
    RIGHT_PAREN = ')'       # single
    LEFT_CURLY = '{'        # single
    RIGHT_CURLY = '}'       # single
    LEFT_SQUARE = '['       # single
    RIGHT_SQUARE = ']'      # single

    # Keywords
    DOT = '.'               # single
    COMMA = ','             # single
    SEMICOLON = ';'         # single

    IDENTIFIER = 'identifier'
    STRING = 'string'
    INT = 'int'
    FLOAT = 'float'

    VAR = 'var'
    FUNCTION = 'func'
    RETURN = 'return'
    IF = 'if'
    ELSE = 'else'
    ELIF = 'elif'
    WHILE = 'while'
    PRINT = 'print'
    INCLUDE = 'include'
    CLASS = 'class'

    # internal tokens
    EOL = 'EOL'             # single
    EOF = 'EOF'
    ERROR = 'ERROR'
    COMMENT = '//'          # double with DIV
    BLOCK_COMMENT = '/*'


reserved_words = {
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
}

single_token = {
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

double_token = {
    '=': {'match': '=', 'yes': TokenType.EQUALITY, 'no': TokenType.EQUALS},
    '!': {'match': '=', 'yes': TokenType.INEQUALITY, 'no': TokenType.NOT},
    '>': {'match': '=', 'yes': TokenType.GTE, 'no': TokenType.GT},
    '<': {'match': '=', 'yes': TokenType.LTE, 'no': TokenType.LT},
    '&': {'match': '&', 'yes': TokenType.AND, 'no': TokenType.ERROR},
    '|': {'match': '|', 'yes': TokenType.OR, 'no': TokenType.ERROR},
}

disregarded_whitespace = {
    ' ', '\r', '\t'
}

end_of_line = {
    '\n'
}

string_literal = {
    '"', "'"
}

number_literal = {
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
}
