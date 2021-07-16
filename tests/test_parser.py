import unittest
from parser import Parser
from tokens import Token, TokenType
from expression import Literal, Unary, Binary


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()
        self.tokens = {
            TokenType.IDENTIFIER: Token(
                TokenType.IDENTIFIER, 'name', 'identifier', 1),
            TokenType.INT: Token(TokenType.INT, '1', 1, 1),
            TokenType.MINUS: Token(TokenType.MINUS, '-', '-', 1),
            TokenType.NOT: Token(TokenType.NOT, '!', '!', 1),
            TokenType.ASTERISK: Token(TokenType.ASTERISK, '*', '*', 1),
            TokenType.DIV: Token(TokenType.DIV, '/', '/', 1),
            TokenType.PLUS: Token(TokenType.PLUS, '+', '+', 1),
            TokenType.GTE: Token(TokenType.GTE, '>=', '>=', 1),
            TokenType.GT: Token(TokenType.GT, '>', '>', 1),
            TokenType.LTE: Token(TokenType.LTE, '<=', '<=', 1),
            TokenType.LT: Token(TokenType.LT, '<', '<', 1),
            TokenType.EQUALITY: Token(TokenType.EQUALITY, '==', '==', 1),
            TokenType.INEQUALITY: Token(TokenType.INEQUALITY, '!=', '!=', 1)
        }

    def test_empty_input(self):
        self.assertEqual(self.parser.parse(), None)

    def test_int_statement(self):
        self.parser.tokens = [self.tokens[TokenType.INT]]

        self.assertEqual(
            self.parser.parse(),
            Literal(self.tokens[TokenType.INT])
        )

    def test_id_statement(self):
        self.parser.tokens = [self.tokens[TokenType.IDENTIFIER]]

        self.assertEqual(
            self.parser.parse(),
            Literal(self.tokens[TokenType.IDENTIFIER])
        )

    def test_unary_minus(self):
        self.parser.tokens = [
            self.tokens[TokenType.MINUS],
            self.tokens[TokenType.INT]
        ]

        self.assertEqual(
            self.parser.parse(),
            Unary(
                self.tokens[TokenType.MINUS],
                Literal(self.tokens[TokenType.INT])
            )
        )

    def test_unary_not(self):
        self.parser.tokens = [
            self.tokens[TokenType.NOT],
            self.tokens[TokenType.INT]
        ]

        self.assertEqual(
            self.parser.parse(),
            Unary(
                self.tokens[TokenType.NOT],
                Literal(self.tokens[TokenType.INT])
            )
        )

    def test_asterisk(self):
        self.parser.tokens = [
            self.tokens[TokenType.IDENTIFIER],
            self.tokens[TokenType.ASTERISK],
            self.tokens[TokenType.INT]
        ]

        self.assertEqual(
            self.parser.parse(),
            Binary(
                Literal(self.tokens[TokenType.IDENTIFIER]),
                self.tokens[TokenType.ASTERISK],
                Literal(self.tokens[TokenType.INT])
            )
        )

    def test_slash(self):
        self.parser.tokens = [
            self.tokens[TokenType.INT],
            self.tokens[TokenType.DIV],
            self.tokens[TokenType.IDENTIFIER]
        ]

        self.assertEqual(
            self.parser.parse(),
            Binary(
                Literal(self.tokens[TokenType.INT]),
                self.tokens[TokenType.DIV],
                Literal(self.tokens[TokenType.IDENTIFIER])
            )
        )

    def test_initial_minus(self):
        self.parser.tokens = [
            self.tokens[TokenType.MINUS],
            self.tokens[TokenType.INT],
            self.tokens[TokenType.DIV],
            self.tokens[TokenType.IDENTIFIER]
        ]

        self.assertEqual(
            self.parser.parse(),
            Binary(
                Unary(
                    self.tokens[TokenType.MINUS],
                    Literal(self.tokens[TokenType.INT])
                ),
                self.tokens[TokenType.DIV],
                Literal(self.tokens[TokenType.IDENTIFIER])
            )
        )

    def test_plus(self):
        self.parser.tokens = [
            self.tokens[TokenType.IDENTIFIER],
            self.tokens[TokenType.PLUS],
            self.tokens[TokenType.IDENTIFIER]
        ]

        self.assertEqual(
            self.parser.parse(),
            Binary(
                Literal(self.tokens[TokenType.IDENTIFIER]),
                self.tokens[TokenType.PLUS],
                Literal(self.tokens[TokenType.IDENTIFIER])
            )
        )

    def test_binary_minus(self):
        self.parser.tokens = [
            self.tokens[TokenType.INT],
            self.tokens[TokenType.MINUS],
            self.tokens[TokenType.INT]
        ]

        self.assertEqual(
            self.parser.parse(),
            Binary(
                Literal(self.tokens[TokenType.INT]),
                self.tokens[TokenType.MINUS],
                Literal(self.tokens[TokenType.INT])
            )
        )

    def test_unary_binary_minuses(self):
        self.parser.tokens = [
            self.tokens[TokenType.MINUS],
            self.tokens[TokenType.IDENTIFIER],
            self.tokens[TokenType.MINUS],
            self.tokens[TokenType.MINUS],
            self.tokens[TokenType.IDENTIFIER]
        ]

        self.assertEqual(
            self.parser.parse(),
            Binary(
                Unary(
                    self.tokens[TokenType.MINUS],
                    Literal(self.tokens[TokenType.IDENTIFIER])
                ),
                self.tokens[TokenType.MINUS],
                Unary(
                    self.tokens[TokenType.MINUS],
                    Literal(self.tokens[TokenType.IDENTIFIER])
                )
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
            Binary(
                Literal(self.tokens[TokenType.INT]),
                self.tokens[TokenType.PLUS],
                Binary(
                    Unary(
                        self.tokens[TokenType.MINUS],
                        Literal(self.tokens[TokenType.INT])
                    ),
                    self.tokens[TokenType.ASTERISK],
                    Literal(self.tokens[TokenType.INT])
                )
            )
        )

    def test_gte(self):
        self.parser.tokens = [
            self.tokens[TokenType.IDENTIFIER],
            self.tokens[TokenType.GTE],
            self.tokens[TokenType.INT]
        ]

        self.assertEqual(
            self.parser.parse(),
            Binary(
                Literal(self.tokens[TokenType.IDENTIFIER]),
                self.tokens[TokenType.GTE],
                Literal(self.tokens[TokenType.INT])
            )
        )

    def test_gt(self):
        self.parser.tokens = [
            self.tokens[TokenType.IDENTIFIER],
            self.tokens[TokenType.GT],
            self.tokens[TokenType.INT]
        ]

        self.assertEqual(
            self.parser.parse(),
            Binary(
                Literal(self.tokens[TokenType.IDENTIFIER]),
                self.tokens[TokenType.GT],
                Literal(self.tokens[TokenType.INT])
            )
        )

    def test_lte(self):
        self.parser.tokens = [
            self.tokens[TokenType.IDENTIFIER],
            self.tokens[TokenType.LTE],
            self.tokens[TokenType.INT]
        ]

        self.assertEqual(
            self.parser.parse(),
            Binary(
                Literal(self.tokens[TokenType.IDENTIFIER]),
                self.tokens[TokenType.LTE],
                Literal(self.tokens[TokenType.INT])
            )
        )

    def test_lt(self):
        self.parser.tokens = [
            self.tokens[TokenType.IDENTIFIER],
            self.tokens[TokenType.LT],
            self.tokens[TokenType.INT]
        ]

        self.assertEqual(
            self.parser.parse(),
            Binary(
                Literal(self.tokens[TokenType.IDENTIFIER]),
                self.tokens[TokenType.LT],
                Literal(self.tokens[TokenType.INT])
            )
        )

    def test_term_then_comparison(self):
        self.parser.tokens = [
            self.tokens[TokenType.IDENTIFIER],
            self.tokens[TokenType.PLUS],
            self.tokens[TokenType.INT],
            self.tokens[TokenType.GT],
            self.tokens[TokenType.INT]
        ]

        self.assertEqual(
            self.parser.parse(),
            Binary(
                Binary(
                    Literal(self.tokens[TokenType.IDENTIFIER]),
                    self.tokens[TokenType.PLUS],
                    Literal(self.tokens[TokenType.INT])
                ),
                self.tokens[TokenType.GT],
                Literal(self.tokens[TokenType.INT])
            )
        )

    def test_equality(self):
        self.parser.tokens = [
            self.tokens[TokenType.IDENTIFIER],
            self.tokens[TokenType.EQUALITY],
            self.tokens[TokenType.INT]
        ]

        self.assertEqual(
            self.parser.parse(),
            Binary(
                Literal(self.tokens[TokenType.IDENTIFIER]),
                self.tokens[TokenType.EQUALITY],
                Literal(self.tokens[TokenType.INT])
            )
        )

    def test_inequality(self):
        self.parser.tokens = [
            self.tokens[TokenType.INT],
            self.tokens[TokenType.INEQUALITY],
            self.tokens[TokenType.IDENTIFIER]
        ]

        self.assertEqual(
            self.parser.parse(),
            Binary(
                Literal(self.tokens[TokenType.INT]),
                self.tokens[TokenType.INEQUALITY],
                Literal(self.tokens[TokenType.IDENTIFIER])
            )
        )


if __name__ == '__main__':
    unittest.main()