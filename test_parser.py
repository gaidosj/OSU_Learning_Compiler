import unittest
from parser import Parser
from tokens import Token
from tokens import TokenType
import expression


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_empty_input(self):
        result = self.parser.parse()
        self.assertEqual(result, None)

    def test_int_statement(self):
        token = Token(TokenType.INT, '0', 0, 1)
        self.parser.tokens = [token]
        result = self.parser.parse()
        expectedResult = expression.Literal(token)
        self.assertEqual(result, expectedResult)

    def test_id_statement(self):
        token = Token(TokenType.IDENTIFIER, 'name', 'identifier', 1)
        self.parser.tokens = [token]
        result = self.parser.parse()
        expectedResult = expression.Literal(token)
        self.assertEqual(result, expectedResult)

    def test_simple_unary(self):
        minus = Token(TokenType.MINUS, '-', '-', 1)
        one = Token(TokenType.INT, '1', 1, 1)
        self.parser.tokens = [minus, one]
        result = self.parser.parse()
        self.assertEqual(
            result,
            expression.Unary(minus, expression.Literal(one))
        )

    def test_simple_factor(self):
        left = Token(TokenType.INT, '2', 2, 1)
        asterisk = Token(TokenType.ASTERISK, '*', '*', 1)
        right = Token(TokenType.IDENTIFIER, 'name', 'identifier', 1)
        self.parser.tokens = [left, asterisk, right]
        result = self.parser.parse()
        self.assertEqual(
            result,
            expression.Binary(
                expression.Literal(left),
                asterisk,
                expression.Literal(right)
            )
        )


if __name__ == '__main__':
    unittest.main()
