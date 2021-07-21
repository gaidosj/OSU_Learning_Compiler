import unittest
from src.parser import Parser
from src.tokens import TokenOsu, TokenType
from src.ast_node_expression import Literal, Unary, Binary
from src.abstract_syntax_tree import AbstractSyntaxTree


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()
        self.tokens = {
            TokenType.IDENTIFIER: TokenOsu(
                TokenType.IDENTIFIER, 'name', 'identifier', 1),
            TokenType.INT: TokenOsu(TokenType.INT, '1', 1, 1),
            TokenType.MINUS: TokenOsu(TokenType.MINUS, '-', '-', 1),
            TokenType.NOT: TokenOsu(TokenType.NOT, '!', '!', 1),
            TokenType.ASTERISK: TokenOsu(TokenType.ASTERISK, '*', '*', 1),
            TokenType.DIV: TokenOsu(TokenType.DIV, '/', '/', 1),
            TokenType.PLUS: TokenOsu(TokenType.PLUS, '+', '+', 1),
            TokenType.GTE: TokenOsu(TokenType.GTE, '>=', '>=', 1),
            TokenType.GT: TokenOsu(TokenType.GT, '>', '>', 1),
            TokenType.LTE: TokenOsu(TokenType.LTE, '<=', '<=', 1),
            TokenType.LT: TokenOsu(TokenType.LT, '<', '<', 1),
            TokenType.EQUALITY: TokenOsu(TokenType.EQUALITY, '==', '==', 1),
            TokenType.INEQUALITY: TokenOsu(TokenType.INEQUALITY, '!=', '!=', 1)
        }

    def test_empty_input(self):
        self.assertEqual(self.parser.parse(), None)

    def test_int_statement(self):
        self.parser.tokens = [self.tokens[TokenType.INT]]

        self.assertEqual(
            self.parser.parse(),
            AbstractSyntaxTree(Literal(self.tokens[TokenType.INT]))
        )

    def test_id_statement(self):
        self.parser.tokens = [self.tokens[TokenType.IDENTIFIER]]

        self.assertEqual(
            self.parser.parse(),
            AbstractSyntaxTree(Literal(self.tokens[TokenType.IDENTIFIER]))
        )

    def test_unary_minus(self):
        self.parser.tokens = [
            self.tokens[TokenType.MINUS],
            self.tokens[TokenType.INT]
        ]

        self.assertEqual(
            self.parser.parse(),
            AbstractSyntaxTree(
                Unary(
                    self.tokens[TokenType.MINUS],
                    Literal(self.tokens[TokenType.INT])
                )
            )
        )

    def test_unary_not(self):
        self.parser.tokens = [
            self.tokens[TokenType.NOT],
            self.tokens[TokenType.INT]
        ]

        self.assertEqual(
            self.parser.parse(),
            AbstractSyntaxTree(
                Unary(
                    self.tokens[TokenType.NOT],
                    Literal(self.tokens[TokenType.INT])
                )
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
            AbstractSyntaxTree(
                Binary(
                    Literal(self.tokens[TokenType.IDENTIFIER]),
                    self.tokens[TokenType.ASTERISK],
                    Literal(self.tokens[TokenType.INT])
                )
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
            AbstractSyntaxTree(
                Binary(
                    Literal(self.tokens[TokenType.INT]),
                    self.tokens[TokenType.DIV],
                    Literal(self.tokens[TokenType.IDENTIFIER])
                )
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
            AbstractSyntaxTree(
                Binary(
                    Unary(
                        self.tokens[TokenType.MINUS],
                        Literal(self.tokens[TokenType.INT])
                    ),
                    self.tokens[TokenType.DIV],
                    Literal(self.tokens[TokenType.IDENTIFIER])
                )
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
            AbstractSyntaxTree(
                Binary(
                    Literal(self.tokens[TokenType.IDENTIFIER]),
                    self.tokens[TokenType.PLUS],
                    Literal(self.tokens[TokenType.IDENTIFIER])
                )
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
            AbstractSyntaxTree(
                Binary(
                    Literal(self.tokens[TokenType.INT]),
                    self.tokens[TokenType.MINUS],
                    Literal(self.tokens[TokenType.INT])
                )
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
            AbstractSyntaxTree(
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
            AbstractSyntaxTree(
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
        )

    def test_gte(self):
        self.parser.tokens = [
            self.tokens[TokenType.IDENTIFIER],
            self.tokens[TokenType.GTE],
            self.tokens[TokenType.INT]
        ]

        self.assertEqual(
            self.parser.parse(),
            AbstractSyntaxTree(
                Binary(
                    Literal(self.tokens[TokenType.IDENTIFIER]),
                    self.tokens[TokenType.GTE],
                    Literal(self.tokens[TokenType.INT])
                )
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
            AbstractSyntaxTree(
                Binary(
                    Literal(self.tokens[TokenType.IDENTIFIER]),
                    self.tokens[TokenType.GT],
                    Literal(self.tokens[TokenType.INT])
                )
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
            AbstractSyntaxTree(
                Binary(
                    Literal(self.tokens[TokenType.IDENTIFIER]),
                    self.tokens[TokenType.LTE],
                    Literal(self.tokens[TokenType.INT])
                )
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
            AbstractSyntaxTree(
                Binary(
                    Literal(self.tokens[TokenType.IDENTIFIER]),
                    self.tokens[TokenType.LT],
                    Literal(self.tokens[TokenType.INT])
                )
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

        result = self.parser.parse()
        self.assertEqual(
            result,
            AbstractSyntaxTree(
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
        )

    def test_equality(self):
        self.parser.tokens = [
            self.tokens[TokenType.IDENTIFIER],
            self.tokens[TokenType.EQUALITY],
            self.tokens[TokenType.INT]
        ]

        self.assertEqual(
            self.parser.parse(),
            AbstractSyntaxTree(
                Binary(
                    Literal(self.tokens[TokenType.IDENTIFIER]),
                    self.tokens[TokenType.EQUALITY],
                    Literal(self.tokens[TokenType.INT])
                )
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
            AbstractSyntaxTree(
                Binary(
                    Literal(self.tokens[TokenType.INT]),
                    self.tokens[TokenType.INEQUALITY],
                    Literal(self.tokens[TokenType.IDENTIFIER])
                )
            )
        )


if __name__ == '__main__':
    unittest.main()
