from tokens import Token, TokenType, \
    single_token, disregarded_whitespace, double_token, end_of_line, reserved_words


class Lexer:
    def __init__(self, source_code=None):
        self.source = source_code
        self.tokens = []
        self.current_source_line = 0
        self.start = 0
        self.current = 0

    def get_source_code(self):
        return self.source

    def get_tokens(self):
        return self.tokens

    def load_source_code(self, source_code):
        self.source = source_code
        self.tokens = []
        self.current_source_line = 0
        self.start = 0
        self.current = 0

    def process_source_code(self):
        self.start = self.current = 0
        while not self._is_at_end():
            self.start = self.current
            self._scan_token()
        self.start = self.current
        self._add_token(TokenType.EOF)

    # ---------------------------------------------------
    # private methods

    def _scan_token(self):
        char = self._advance()

        if char in disregarded_whitespace:
            return

        if char in end_of_line:
            self.current_source_line += 1

        if char in double_token:
            expected_match = double_token[char]['match']
            token1 = double_token[char]['yes']
            token2 = double_token[char]['no']
            self._add_token(token1 if self._match(expected_match) else token2)
            return

        if char in single_token:
            self._add_token(single_token[char])
            return

        # // comments
        if char == '/':
            if self._match('/'):
                self._match_until('\n')
                self._add_token(TokenType.COMMENT)
            else:
                self._add_token(TokenType.DIV)
            return

        # string literals
        if char == "'" or char == '"':
            self._add_token_string_literal(closing_char=char)
            return

        # number literals
        if char.isdigit():
            self._add_token_number_literal()
            return

        # identifiers and reserved words
        if char.isalpha() or char == '_':
            self._add_token_identifier_or_reserved_word()
            return

        # at this point no valid tokens are possible
        if self.tokens and self.tokens[-1].type == TokenType.ERROR:
            # if last token is ERROR -> extend its lexeme
            self.tokens[-1].lexeme += self.source[self.start: self.current]
        else:
            # otherwise -> start new ERROR token
            self._add_token(TokenType.ERROR, 'Unexpected token')


    # ---------------------------------------------------

    def _match_until(self, expected_char):
        while self._peek() != expected_char and not self._is_at_end():
            self._advance()

    def _is_at_end(self):
        return self.current >= len(self.source)

    def _peek(self):
        if self._is_at_end():
            return None
        return self.source[self.current]

    def _peek_next(self):
        if self.current + 1 > len(self.source):
            return None
        return self.source[self.current + 1]

    def _advance(self):
        if self._is_at_end():
            return None
        self.current += 1
        return self.source[self.current - 1]

    def _match(self, expected_char):
        if self._peek() != expected_char:
            return False
        self.current += 1
        return True

    def _add_token(self, token_type, literal=None):
        lexeme = self.source[self.start: self.current]
        self.tokens.append(Token(token_type, lexeme, literal))

    def _add_token_string_literal(self, closing_char):
        while self._peek() != closing_char and not self._is_at_end():
            if self._peek() in end_of_line:
                self.current_source_line += 1
            self._advance()

        if self._is_at_end():
            self._add_token(TokenType.ERROR, 'Unterminated string')
            return

        # skip over string closing symbol
        self._advance()

        string_value = self.source[self.start + 1: self.current -1]
        self._add_token(TokenType.STRING, string_value)

    def _add_token_number_literal(self):
        while self._peek() and self._peek().isdigit():
            self._advance()

        if self._peek() == '.' and self._peek_next().isdigit():
            self._advance()
            while self._peek() and self._peek().isdigit():
                self._advance()
            value = float(self.source[self.start: self.current])
            self._add_token(TokenType.FLOAT, value)
        else:
            value = int(self.source[self.start: self.current])
            self._add_token(TokenType.INT, value)

    def _add_token_identifier_or_reserved_word(self):
        while self._peek() and self._peek().isalpha() or self._peek() == '_':
            self._advance()

        lexeme = self.source[self.start: self.current]
        if lexeme in reserved_words:
            self._add_token(reserved_words[lexeme])
        else:
            self._add_token(TokenType.IDENTIFIER)


if __name__ == '__main__':
    test_cases = (
        '() {} * ==\n = != =//! // hello',
        '+ "WELCOME" \'HELLO\' 123 123.1 123.0 0 0.0',
        'hello = 20; print 30 && || & | ! 25.0 * _some_string"'
    )

    lexer = Lexer()
    for source_code in test_cases:
        lexer.load_source_code(source_code)
        lexer.process_source_code()

        print('\nSOURCE CODE:\n', source_code)
        print('\nTOKENS:')
        for token in lexer.get_tokens():
            if token.type in (TokenType.EOL, TokenType.EOF):
                print(token.type.name)
            else:
                print('{} \'{}\'     '.format(token.type.name, token.lexeme), end='')
