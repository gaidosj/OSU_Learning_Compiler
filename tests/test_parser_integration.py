import unittest
import os
from src.lexer import Lexer
from src.parser import Parser
from src.abstract_syntax_tree import AbstractSyntaxTree


class ParserIntegrationTest(unittest.TestCase):
    def test_with_olc_source_files(self):
        """
        Testing with .olc source files. Comparing output with the prepared .ast files
        """
        test_programs = (
            'program_01',
            'program_02',
            'program_03',
        )

        for filename in test_programs:

            full_name = os.path.join(os.path.dirname(__file__), 'olc_programs/{}.olc'.format(filename))
            with open(full_name, 'r') as input_handle:
                source_code = input_handle.read()

                lexer = Lexer(source_code)
                lexer.process_source_code()
                tokens = lexer.get_tokens()

                parser = Parser(tokens)
                actual_parsed_code = '\n'.join(
                    [str(AbstractSyntaxTree(statement)) for statement in parser.parse()]
                ) + '\n'

            full_name = os.path.join(os.path.dirname(__file__), 'olc_programs/{}.ast'.format(filename))
            with open(full_name, 'r') as input_handle:
                expected_parsed_code = input_handle.read()

            # print(source_code)
            # print(tokens)
            # print(actual_parsed_code)
            self.assertEqual(expected_parsed_code, actual_parsed_code)


if __name__ == '__main__':
    unittest.main()
