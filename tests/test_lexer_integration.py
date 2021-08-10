import unittest
import os
from src.lexer import Lexer


class LexerIntegrationTest(unittest.TestCase):
    def test_with_olc_source_files(self):
        """
        Testing with .olc source files. Comparing output with the prepared .lex files
        """
        test_programs = (
            'program_01',
            'program_02',
            'program_03',
            'program_04',
        )

        for filename in test_programs:

            full_name = os.path.join(os.path.dirname(__file__), 'olc_programs/{}.olc'.format(filename))
            with open(full_name, 'r') as input_handle:
                source_code = input_handle.read()
                lexer = Lexer(source_code)
                lexer.scan()
                token_string = lexer.get_tokens_as_string()

            full_name = os.path.join(os.path.dirname(__file__), 'olc_programs/{}.lex'.format(filename))
            with open(full_name, 'r') as input_handle:
                expected_token_string = input_handle.read()

            # print(source_code)
            # print(token_string)
            # print(expected_token_string)
            self.assertEqual(token_string, expected_token_string)


if __name__ == '__main__':
    unittest.main()
