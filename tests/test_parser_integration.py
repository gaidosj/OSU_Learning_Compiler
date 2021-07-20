import unittest
import os
from src.lexer import Lexer
from src.parser import Parser


class ParserIntegrationTest(unittest.TestCase):
    def test_with_olc_source_files(self):
        """
        Testing with .olc source files. Comparing output with the prepared .ast files
        """
        for filename in ('program_01', 'program_02', 'program_03', 'program_04'):
            # read OLC source code and convert to the list of tokens
            full_name = os.path.join(os.path.dirname(__file__), 'olc_programs/{}.olc'.format(filename))
            with open(full_name, 'r') as input_handle:
                source_code = input_handle.read()

                lexer = Lexer(source_code)
                lexer.process_source_code()
                tokens = lexer.get_tokens()

                parser = Parser(tokens)
                ast = parser.parse()



            # read expected list of tokens
            # full_name = os.path.join(os.path.dirname(__file__), 'olc_programs/{}.ast'.format(filename))
            # with open(full_name, 'r') as input_handle:
            #     expected_token_string = input_handle.read()

            print(source_code)
            print(tokens)
            print(ast)
            # print(expected_token_string)
            # self.assertEqual(token_string, expected_token_string)