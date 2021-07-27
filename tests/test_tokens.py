import unittest
from src.tokens import TokenOsu, TokenType


class TokenTestCase(unittest.TestCase):
    def test_string_representation_of_tokens(self):
        """
        Testing string representation of all token types (retuns of str() method called on the token object).
        String representation of individual tokens is relied upon in the subsequent tests of the lexer.
        """
        test_cases = (
            (TokenOsu(TokenType.EQUALS, '='), "EQUALS '='"),
            (TokenOsu(TokenType.PLUS, '+'), "PLUS '+'"),
            (TokenOsu(TokenType.MINUS, '-'), "MINUS '-'"),
            (TokenOsu(TokenType.ASTERISK, '*'), "ASTERISK '*'"),
            (TokenOsu(TokenType.DIV, '/'), "DIV '/'"),
            (TokenOsu(TokenType.EXPONENT, '**'), "EXPONENT '**'"),
            (TokenOsu(TokenType.REMAINDER, '%'), "REMAINDER '%'"),

            (TokenOsu(TokenType.LT, '<'), "LT '<'"),
            (TokenOsu(TokenType.LTE, '<='), "LTE '<='"),
            (TokenOsu(TokenType.GT, '>'), "GT '>'"),
            (TokenOsu(TokenType.GTE, '>='), "GTE '>='"),
            (TokenOsu(TokenType.EQUALITY, '=='), "EQUALITY '=='"),
            (TokenOsu(TokenType.INEQUALITY, '!='), "INEQUALITY '!='"),

            (TokenOsu(TokenType.NOT, '!'), "NOT '!'"),
            (TokenOsu(TokenType.AND, '&&'), "AND '&&'"),
            (TokenOsu(TokenType.OR, '||'), "OR '||'"),
            (TokenOsu(TokenType.XOR, '^'), "XOR '^'"),

            (TokenOsu(TokenType.LEFT_PAREN, '('), "LEFT_PAREN '('"),
            (TokenOsu(TokenType.RIGHT_PAREN, ')'), "RIGHT_PAREN ')'"),
            (TokenOsu(TokenType.LEFT_CURLY, '{'), "LEFT_CURLY '{'"),
            (TokenOsu(TokenType.RIGHT_CURLY, '}'), "RIGHT_CURLY '}'"),
            (TokenOsu(TokenType.LEFT_SQUARE, '['), "LEFT_SQUARE '['"),
            (TokenOsu(TokenType.RIGHT_SQUARE, ']'), "RIGHT_SQUARE ']'"),

            (TokenOsu(TokenType.DOT, '.'), "DOT '.'"),
            (TokenOsu(TokenType.COMMA, ','), "COMMA ','"),
            (TokenOsu(TokenType.SEMICOLON, ';'), "SEMICOLON ';'"),

            (TokenOsu(TokenType.IDENTIFIER, 'abcd', 'abcd'), "IDENTIFIER 'abcd' val=abcd"),
            (TokenOsu(TokenType.IDENTIFIER, '_var_name', '_var_name'), "IDENTIFIER '_var_name' val=_var_name"),
            (TokenOsu(TokenType.IDENTIFIER, '__', '__'), "IDENTIFIER '__' val=__"),
            (TokenOsu(TokenType.IDENTIFIER, '_Aa_bB', '_Aa_bB'), "IDENTIFIER '_Aa_bB' val=_Aa_bB"),
            (TokenOsu(TokenType.IDENTIFIER, 'Aa_bB', 'Aa_bB'), "IDENTIFIER 'Aa_bB' val=Aa_bB"),

            (TokenOsu(TokenType.STRING, '\'abcd\'', 'abcd'), "STRING ''abcd'' val=abcd"),
            (TokenOsu(TokenType.STRING, '"abcd"', 'abcd'), "STRING '\"abcd\"' val=abcd"),

            (TokenOsu(TokenType.INT, '123', 123), "INT '123' val=123"),
            (TokenOsu(TokenType.INT, '0', 0), "INT '0' val=0"),

            (TokenOsu(TokenType.FLOAT, '123.1', 123.1), "FLOAT '123.1' val=123.1"),
            (TokenOsu(TokenType.FLOAT, '123.0', 123.0), "FLOAT '123.0' val=123.0"),
            (TokenOsu(TokenType.FLOAT, '0.0', 0.0), "FLOAT '0.0' val=0.0"),

            (TokenOsu(TokenType.VAR, 'var'), "VAR 'var'"),
            (TokenOsu(TokenType.FUNCTION, 'function'), "FUNCTION 'function'"),
            (TokenOsu(TokenType.RETURN, 'return'), "RETURN 'return'"),
            (TokenOsu(TokenType.IF, 'if'), "IF 'if'"),
            (TokenOsu(TokenType.ELSE, 'else'), "ELSE 'else'"),
            (TokenOsu(TokenType.ELIF, 'elif'), "ELIF 'elif'"),
            (TokenOsu(TokenType.WHILE, 'while'), "WHILE 'while'"),
            (TokenOsu(TokenType.PRINT, 'print'), "PRINT 'print'"),
            (TokenOsu(TokenType.INCLUDE, 'include'), "INCLUDE 'include'"),
            (TokenOsu(TokenType.CLASS, 'class'), "CLASS 'class'"),

            (TokenOsu(TokenType.EOL, '\n'), "EOL\n"),
            (TokenOsu(TokenType.EOF, ''), "EOF"),
            (TokenOsu(TokenType.ERROR, ''), "ERROR ''"),
            (TokenOsu(TokenType.COMMENT, '// my comment'), "COMMENT '// my comment'"),
        )
        for token, expected_string_representation in test_cases:
            self.assertEqual('{}'.format(token), expected_string_representation)


if __name__ == '__main__':
    unittest.main()
