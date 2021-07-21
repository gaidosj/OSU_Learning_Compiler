from src.tokens import TokenType

IGNORED_TOKENS = {
    TokenType.EOF,
    TokenType.EOL,
    TokenType.ERROR,
    TokenType.COMMENT,
    TokenType.BLOCK_COMMENT,
}

EQUALITY_TOKENS = {
    TokenType.EQUALITY,
    TokenType.INEQUALITY,
}

COMPARISON_TOKENS = {
    TokenType.LT,
    TokenType.LTE,
    TokenType.GT,
    TokenType.GTE,
}

TERM_TOKENS = {
    TokenType.PLUS,
    TokenType.MINUS,
}

FACTOR_TOKENS = {
    TokenType.ASTERISK,
    TokenType.DIV,
}

UNARY_TOKENS = {
    TokenType.NOT,
    TokenType.MINUS,
}

PRIMARY_TOKENS = {
    TokenType.INT,
    TokenType.FLOAT,
    TokenType.STRING,
    TokenType.IDENTIFIER,
}

PAREN_OPENING = {
    TokenType.LEFT_PAREN,
}

PAREN_CLOSING = {
    TokenType.RIGHT_PAREN,
}

STARTING_TOKENS = {
    TokenType.CLASS,
    TokenType.FUNCTION,
    TokenType.VAR,
    TokenType.IF,
    TokenType.WHILE,
    TokenType.PRINT,
    TokenType.RETURN,
}

# TODO: Classify and / or implement later
UNCLASSIFIED_TOKENS = {
    'exponent **',
    'mod %',
    TokenType.AND,
    TokenType.XOR,
    TokenType.OR,
    'TRUE',
    'FALSE',
    'NULL'
}
