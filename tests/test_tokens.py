import unittest
from src.tokens import TokenOsu, TokenType


class TokenTestCase(unittest.TestCase):
    def test_string_representation_of_tokens(self):
        """
        Testing string representation of all token types (retuns of str() method called on the token object).
        String representation of individual tokens is relied upon in the subsequent tests of the lexer.
        """
        test_cases = (
            (TokenOsu(TokenType.EQUALS, '='), "TOKEN.EQUALS '='"),
            (TokenOsu(TokenType.PLUS, '+'), "TOKEN.PLUS '+'"),
            (TokenOsu(TokenType.MINUS, '-'), "TOKEN.MINUS '-'"),
            (TokenOsu(TokenType.ASTERISK, '*'), "TOKEN.ASTERISK '*'"),
            (TokenOsu(TokenType.DIV, '/'), "TOKEN.DIV '/'"),

            (TokenOsu(TokenType.LT, '<'), "TOKEN.LT '<'"),
            (TokenOsu(TokenType.LTE, '<='), "TOKEN.LTE '<='"),
            (TokenOsu(TokenType.GT, '>'), "TOKEN.GT '>'"),
            (TokenOsu(TokenType.GTE, '>='), "TOKEN.GTE '>='"),
            (TokenOsu(TokenType.EQUALITY, '=='), "TOKEN.EQUALITY '=='"),
            (TokenOsu(TokenType.INEQUALITY, '!='), "TOKEN.INEQUALITY '!='"),

            (TokenOsu(TokenType.NOT, '!'), "TOKEN.NOT '!'"),
            (TokenOsu(TokenType.AND, '&&'), "TOKEN.AND '&&'"),
            (TokenOsu(TokenType.OR, '||'), "TOKEN.OR '||'"),
            (TokenOsu(TokenType.XOR, '^'), "TOKEN.XOR '^'"),

            (TokenOsu(TokenType.LEFT_PAREN, '('), "TOKEN.LEFT_PAREN '('"),
            (TokenOsu(TokenType.RIGHT_PAREN, ')'), "TOKEN.RIGHT_PAREN ')'"),
            (TokenOsu(TokenType.LEFT_CURLY, '{'), "TOKEN.LEFT_CURLY '{'"),
            (TokenOsu(TokenType.RIGHT_CURLY, '}'), "TOKEN.RIGHT_CURLY '}'"),
            (TokenOsu(TokenType.LEFT_SQUARE, '['), "TOKEN.LEFT_SQUARE '['"),
            (TokenOsu(TokenType.RIGHT_SQUARE, ']'), "TOKEN.RIGHT_SQUARE ']'"),

            (TokenOsu(TokenType.DOT, '.'), "TOKEN.DOT '.'"),
            (TokenOsu(TokenType.COMMA, ','), "TOKEN.COMMA ','"),
            (TokenOsu(TokenType.SEMICOLON, ';'), "TOKEN.SEMICOLON ';'"),

            (TokenOsu(TokenType.IDENTIFIER, 'abcd', 'abcd'), "TOKEN.IDENTIFIER 'abcd' val=abcd"),
            (TokenOsu(TokenType.IDENTIFIER, '_var_name', '_var_name'), "TOKEN.IDENTIFIER '_var_name' val=_var_name"),
            (TokenOsu(TokenType.IDENTIFIER, '__', '__'), "TOKEN.IDENTIFIER '__' val=__"),
            (TokenOsu(TokenType.IDENTIFIER, '_Aa_bB', '_Aa_bB'), "TOKEN.IDENTIFIER '_Aa_bB' val=_Aa_bB"),

            (TokenOsu(TokenType.STRING, '\'abcd\'', 'abcd'), "TOKEN.STRING ''abcd'' val=abcd"),
            (TokenOsu(TokenType.STRING, '"abcd"', 'abcd'), "TOKEN.STRING '\"abcd\"' val=abcd"),

            (TokenOsu(TokenType.INT, '123', 123), "TOKEN.INT '123' val=123"),
            (TokenOsu(TokenType.INT, '0', 0), "TOKEN.INT '0' val=0"),

            (TokenOsu(TokenType.FLOAT, '123.1', 123.1), "TOKEN.FLOAT '123.1' val=123.1"),
            (TokenOsu(TokenType.FLOAT, '123.0', 123.0), "TOKEN.FLOAT '123.0' val=123.0"),
            (TokenOsu(TokenType.FLOAT, '0.0', 0.0), "TOKEN.FLOAT '0.0' val=0.0"),

            (TokenOsu(TokenType.VAR, 'var'), "TOKEN.VAR 'var'"),
            (TokenOsu(TokenType.FUNCTION, 'function'), "TOKEN.FUNCTION 'function'"),
            (TokenOsu(TokenType.RETURN, 'return'), "TOKEN.RETURN 'return'"),
            (TokenOsu(TokenType.IF, 'if'), "TOKEN.IF 'if'"),
            (TokenOsu(TokenType.ELSE, 'else'), "TOKEN.ELSE 'else'"),
            (TokenOsu(TokenType.ELIF, 'elif'), "TOKEN.ELIF 'elif'"),
            (TokenOsu(TokenType.WHILE, 'while'), "TOKEN.WHILE 'while'"),
            (TokenOsu(TokenType.PRINT, 'print'), "TOKEN.PRINT 'print'"),
            (TokenOsu(TokenType.INCLUDE, 'include'), "TOKEN.INCLUDE 'include'"),
            (TokenOsu(TokenType.CLASS, 'class'), "TOKEN.CLASS 'class'"),

            (TokenOsu(TokenType.EOL, '\n'), "TOKEN.EOL\n"),
            (TokenOsu(TokenType.EOF, ''), "TOKEN.EOF\n"),
            (TokenOsu(TokenType.ERROR, ''), "TOKEN.ERROR ''"),
            (TokenOsu(TokenType.COMMENT, '// my comment'), "TOKEN.COMMENT '// my comment'"),
            (TokenOsu(TokenType.BLOCK_COMMENT, '/* block cmnt */'), "TOKEN.BLOCK_COMMENT '/* block cmnt */'"),
        )
        for token, expected_string_representation in test_cases:
            self.assertEqual('{}'.format(token), expected_string_representation)


if __name__ == '__main__':
    unittest.main()
