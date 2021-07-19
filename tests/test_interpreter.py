import parent_dir
import unittest
from src.interpreter import Interpreter
from src.expression import Binary, Literal, Unary
from src.tokens import TokenOsu, TokenType


class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()
        self.ints = [
            TokenOsu(TokenType.INT, '0', 0, 1),
            TokenOsu(TokenType.INT, '1', 1, 1),
            TokenOsu(TokenType.INT, '2', 2, 1),
            TokenOsu(TokenType.INT, '3', 3, 1),
            TokenOsu(TokenType.INT, '4', 4, 1),
            TokenOsu(TokenType.INT, '5', 5, 1)
        ]
        self.operators = {
            '-': TokenOsu(TokenType.MINUS, '-', '-', 1),
            '!': TokenOsu(TokenType.NOT, '!', '!', 1),
            '*': TokenOsu(TokenType.ASTERISK, '*', '*', 1),
            '/': TokenOsu(TokenType.DIV, '/', '/', 1),
            '+': TokenOsu(TokenType.PLUS, '+', '+', 1),
            '>=': TokenOsu(TokenType.GTE, '>=', '>=', 1),
            '>': TokenOsu(TokenType.GT, '>', '>', 1),
            '<=': TokenOsu(TokenType.LTE, '<=', '<=', 1),
            '<': TokenOsu(TokenType.LT, '<', '<', 1),
            '==': TokenOsu(TokenType.EQUALITY, '==', '==', 1),
            '!=': TokenOsu(TokenType.INEQUALITY, '!=', '!=', 1)
        }

    def test_one_plus_one(self):
        ast = Binary(
            Literal(self.ints[1]),
            self.operators['+'],
            Literal(self.ints[1])
        )

        self.assertEqual(self.interpreter.interpret(ast), 2)

    def test_five_minus_negative_two_times_three(self):
        ast = Binary(
            Literal(self.ints[5]),
            self.operators['-'],
            Binary(
                Unary(
                    self.operators['-'],
                    Literal(self.ints[2])
                ),
                self.operators['*'],
                Literal(self.ints[3])
            )
        )

        self.assertEqual(self.interpreter.interpret(ast), 11)

    def test_gt(self):
        ast = Binary(
            Literal(self.ints[4]),
            self.operators['>'],
            Literal(self.ints[3])
        )

        self.assertTrue(self.interpreter.interpret(ast))

    def test_equality(self):
        ast = Binary(
            Literal(self.ints[0]),
            self.operators['=='],
            Literal(self.ints[0])
        )

        self.assertTrue(self.interpreter.interpret(ast))


if __name__ == '__main__':
    unittest.main()
    parent_dir
