import unittest
from parser import Parser
from tokens import Token
from tokens import TokenType
import expression


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()
        self.tokens = {
            TokenType.IDENTIFIER: Token(
                TokenType.IDENTIFIER, 'name', 'identifier', 1),
            TokenType.INT: Token(TokenType.INT, '1', 1, 1),
            TokenType.MINUS: Token(TokenType.MINUS, '-', '-', 1),
            TokenType.ASTERISK: Token(TokenType.ASTERISK, '*', '*', 1),
            TokenType.DIV: Token(TokenType.DIV, '/', '/', 1),
            TokenType.PLUS: Token(TokenType.PLUS, '+', '+', 1)
        }

    def test_empty_input(self):
        self.assertEqual(self.parser.parse(), None)

    def test_int_statement(self):
        self.parser.tokens = [self.tokens[TokenType.INT]]

        self.assertEqual(
            self.parser.parse(),
            expression.Literal(self.tokens[TokenType.INT])
        )

    def test_id_statement(self):
        self.parser.tokens = [self.tokens[TokenType.IDENTIFIER]]

        self.assertEqual(
            self.parser.parse(),
            expression.Literal(self.tokens[TokenType.IDENTIFIER])
        )

    def test_simple_unary(self):
        self.parser.tokens = [
            self.tokens[TokenType.MINUS],
            self.tokens[TokenType.INT]
        ]

        self.assertEqual(
            self.parser.parse(),
            expression.Unary(
                self.tokens[TokenType.MINUS],
                expression.Literal(self.tokens[TokenType.INT])
            )
        )

    def test_simple_factor(self):
        self.parser.tokens = [
            self.tokens[TokenType.IDENTIFIER],
            self.tokens[TokenType.ASTERISK],
            self.tokens[TokenType.INT]
        ]

        self.assertEqual(
            self.parser.parse(),
            expression.Binary(
                expression.Literal(self.tokens[TokenType.IDENTIFIER]),
                self.tokens[TokenType.ASTERISK],
                expression.Literal(self.tokens[TokenType.INT])
            )
        )

    def test_unary_inside_factor(self):
        self.parser.tokens = [
            self.tokens[TokenType.MINUS],
            self.tokens[TokenType.INT],
            self.tokens[TokenType.DIV],
            self.tokens[TokenType.IDENTIFIER]
        ]

        self.assertEqual(
            self.parser.parse(),
            expression.Binary(
                expression.Unary(
                    self.tokens[TokenType.MINUS],
                    expression.Literal(self.tokens[TokenType.INT])
                ),
                self.tokens[TokenType.DIV],
                expression.Literal(self.tokens[TokenType.IDENTIFIER])
            )
        )

    def test_simple_term(self):
        self.parser.tokens = [
            self.tokens[TokenType.IDENTIFIER],
            self.tokens[TokenType.PLUS],
            self.tokens[TokenType.IDENTIFIER]
        ]

        self.assertEqual(
            self.parser.parse(),
            expression.Binary(
                expression.Literal(self.tokens[TokenType.IDENTIFIER]),
                self.tokens[TokenType.PLUS],
                expression.Literal(self.tokens[TokenType.IDENTIFIER])
            )
        )

    def test_term_then_factor(self):
        self.parser.tokens = [
            self.tokens[TokenType.INT],
            self.tokens[TokenType.PLUS],
            self.tokens[TokenType.MINUS],
            self.tokens[TokenType.INT],
            self.tokens[TokenType.ASTERISK],
            self.tokens[TokenType.INT]
        ]

        self.assertEqual(
            self.parser.parse(),
            expression.Binary(
                expression.Literal(self.tokens[TokenType.INT]),
                self.tokens[TokenType.PLUS],
                expression.Binary(
                    expression.Unary(
                        self.tokens[TokenType.MINUS],
                        expression.Literal(self.tokens[TokenType.INT])
                    ),
                    self.tokens[TokenType.ASTERISK],
                    expression.Literal(self.tokens[TokenType.INT])
                )
            )
        )


if __name__ == '__main__':
    unittest.main()
