from src.tokens import TokenType

VAR_STATEMENT_TOKENS = {
    TokenType.VAR
}

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

LITERAL_TOKENS = {
    TokenType.INT,
    TokenType.FLOAT,
    TokenType.STRING,
    TokenType.BOOL,
    TokenType.NULL,
}

IDENTIFIER_TOKENS = {
    TokenType.IDENTIFIER
}

EQUALS_TOKENS = {
    TokenType.EQUALS
}

GROUP_OPENING_TOKENS = {
    TokenType.LEFT_PAREN,
}

GROUP_CLOSING_TOKENS = {
    TokenType.RIGHT_PAREN,
}

BLOCK_OPENING_TOKENS = {
    TokenType.LEFT_CURLY,
}

BLOCK_CLOSING_TOKENS = {
    TokenType.RIGHT_CURLY,
}

STATEMENT_END_TOKENS = {
    TokenType.SEMICOLON
}

STATEMENT_START_TOKENS = {
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
}
