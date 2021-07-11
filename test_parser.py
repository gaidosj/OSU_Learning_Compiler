import unittest
from parser import Parser
from tokens import Token
from tokens import TokenType
import expression


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_empty_input(self):
        self.parser.parse()

    def test_int_statement(self):
        token = Token(TokenType.INT, '0', 0, 1)
        self.parser.tokens = [token]
        result = self.parser.parse()
        expectedResult = expression.Literal(0)
        self.assertEqual(result, expectedResult)

    def test_id_statement(self):
        token = Token(TokenType.IDENTIFIER, 'name', 'identifier', 1)
        self.parser.tokens = [token]
        result = self.parser.parse()
        expectedResult = expression.Literal('identifier')
        self.assertEqual(result, expectedResult)


if __name__ == '__main__':
    unittest.main()
