import unittest
from src.lexer import Lexer
from src.tokens import TokenType


class LexerTest(unittest.TestCase):
    @classmethod
    def _get_tokens_as_string(self, tokens_list):
        return ''.join([str(tkn) + '; ' * (tkn.token_type not in (TokenType.EOL, TokenType.EOF)) for tkn in tokens_list])

    def test_basic_lexem_combinations(self):
        """
        Testing with small combinations of 2-5 tokens
        """
        test_cases = (
            ("()", "LEFT_PAREN '('; RIGHT_PAREN ')'; EOF"),
            ("[ ]", "LEFT_SQUARE '['; RIGHT_SQUARE ']'; EOF"),
            (" {   } ", "LEFT_CURLY '{'; RIGHT_CURLY '}'; EOF"),
            ("2 - 2", "INT '2' val=2; MINUS '-'; INT '2' val=2; EOF"),
            ("1 + 1", "INT '1' val=1; PLUS '+'; INT '1' val=1; EOF"),
            ("0.0 * 2", "FLOAT '0.0' val=0.0; ASTERISK '*'; INT '2' val=2; EOF"),
            ("1 / 4.0", "INT '1' val=1; DIV '/'; FLOAT '4.0' val=4.0; EOF"),

            ("function {}", "FUNCTION 'function'; LEFT_CURLY '{'; RIGHT_CURLY '}'; EOF"),
            ("var a = 10", "VAR 'var'; IDENTIFIER 'a'; EQUALS '='; INT '10' val=10; EOF"),
            ("var a = b + c", "VAR 'var'; IDENTIFIER 'a'; EQUALS '='; IDENTIFIER 'b'; PLUS '+'; IDENTIFIER 'c'; EOF"),
            (
                "_private_var = 10 / cA",
                "IDENTIFIER '_private_var'; EQUALS '='; INT '10' val=10; DIV '/'; IDENTIFIER 'cA'; EOF"
            ),
            ("// comment to end of line", "COMMENT '// comment to end of line'; EOF"),
            ("TRUE FALSE NULL", "BOOL 'TRUE'; BOOL 'FALSE'; NULL 'NULL'; EOF"),
        )

        for source_code, expected_token_string in test_cases:
            lexer = Lexer(source_code)
            lexer.scan()
            token_string = lexer.get_tokens_as_string()
            # print(token_string)
            self.assertEqual(token_string, expected_token_string)


if __name__ == '__main__':
    unittest.main()
