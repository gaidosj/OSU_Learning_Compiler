import unittest
from abstract_syntax_tree import AbstractSyntaxTree
from tokens import Token, TokenType
from expression import Literal, Unary, Binary


class AstTest(unittest.TestCase):
    def setUp(self):
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
