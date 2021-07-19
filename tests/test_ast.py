import unittest
from src.abstract_syntax_tree import AbstractSyntaxTree
from src.tokens import TokenOsu, TokenType
from src.parser_expression import Literal, Unary, Binary


class AstTest(unittest.TestCase):
    def setUp(self):
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

    def test_mult_minus(self):
        self.assertEqual(
            str(
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
            ),
            '(1 + ((-1) * 1))'
        )

    def test_plus_gt(self):
        self.assertEqual(
            str(
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
            ),
            '((identifier + 1) > 1)'
        )

    def test_minus_minuses(self):
        self.assertEqual(
            str(
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
            ),
            '((-identifier) - (-identifier))'
        )


if __name__ == '__main__':
    unittest.main()
