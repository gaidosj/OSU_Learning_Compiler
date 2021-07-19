from enum import Enum


class TokenOsu:
    def __init__(self, token_type, lexeme, literal=None, source_file_line_number=0):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.source_file_line_number = source_file_line_number

    def __str__(self):
        if self.token_type in (TokenType.EOL, TokenType.EOF):
            return 'TOKEN.{}\n'.format(self.token_type.name)
        else:
            out = 'TOKEN.{} \'{}\''.format(self.token_type.name, self.lexeme)
            if self.literal is not None:
                out += ' val={}'.format(self.literal)
            return out

    def __repr__(self):
        if self.token_type in (TokenType.EOL, TokenType.EOF):
            return 'TOKEN.{}\n'.format(self.token_type.name)
        else:
            return 'TOKEN.{} (lexeme=\'{}\' literal=\'{}\')'.format(self.token_type.name, self.lexeme, self.literal)


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
