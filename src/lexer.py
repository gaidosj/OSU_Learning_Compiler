from src.tokens import TokenOsu, TokenType
from src.lexer_constants import SINGLE_TOKENS, DOUBLE_TOKENS, \
    DISREGARDED_WHITESPACES, RESERVED_WORDS, END_OF_LINE, \
    STRING_LITERALS, NUMBER_LITERALS, IDENTIFIER_LITERALS


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

    def _scan_token(self):
        char = self._advance()
        self.current_source_line += char == END_OF_LINE

        if char in DISREGARDED_WHITESPACES:
            pass
        elif char in DOUBLE_TOKENS:
            self._add_double_token(char)
        elif char in SINGLE_TOKENS:
            self._add_token(SINGLE_TOKENS[char])
        elif char == '/':
            self._add_token_comment_or_division()
        elif char in STRING_LITERALS:
            self._add_token_string_literal(closing_char=char)
        elif char in NUMBER_LITERALS:
            self._add_token_number_literal()
        elif char in IDENTIFIER_LITERALS:
            self._add_token_identifier_or_reserved_word()
        else:
            self._add_unexpected_token_error()

    def _add_token(self, token_type, literal=None):
        lexeme = self.source[self.start: self.current]
        self.tokens.append(TokenOsu(token_type, lexeme, literal))

    def _add_unexpected_token_error(self):
        if self.tokens and self.tokens[-1].token_type == TokenType.ERROR:
            # if last token is ERROR -> extend its lexeme
            self.tokens[-1].lexeme += self.source[self.start: self.current]
        else:
            # otherwise -> start new ERROR token
            self._add_token(TokenType.ERROR, 'Unexpected token')

    def _add_double_token(self, first_char):
        expected_match = DOUBLE_TOKENS[first_char]['match']
        token1 = DOUBLE_TOKENS[first_char]['yes']
        token2 = DOUBLE_TOKENS[first_char]['no']
        self._add_token(token1 if self._match(expected_match) else token2)

    def _add_token_comment_or_division(self):
        if self._match('/'):
            self._match_until(END_OF_LINE)
            self._add_token(TokenType.COMMENT)
        else:
            self._add_token(TokenType.DIV)

    def _add_token_string_literal(self, closing_char):
        while self._peek() != closing_char and not self._is_at_end():
            self.current_source_line += self._peek() == END_OF_LINE
            self._advance()

        if self._is_at_end():
            self._add_token(TokenType.ERROR, 'Unterminated string')
            return

        # skip over string closing symbol
        self._advance()

        string_value = self.source[self.start + 1: self.current - 1]
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
        while self._peek() and self._peek() in IDENTIFIER_LITERALS:
            self._advance()

        lexeme = self.source[self.start: self.current]
        if lexeme in RESERVED_WORDS:
            self._add_token(RESERVED_WORDS[lexeme])
        else:
            self._add_token(TokenType.IDENTIFIER)

    def _match_until(self, expected_char):
        while self._peek() != expected_char and not self._is_at_end():
            self._advance()

    def _is_at_end(self):
        """
        Return True if the cursor is at the end of the source code
        """
        return self.current >= len(self.source)

    def _peek(self):
        """
        Return source code character from the current cursor position
        without advancing the cursor
        """
        return self.source[self.current] if not self._is_at_end() else None

    def _peek_next(self):
        """
        Return source code character from the position immedeately after
        the current cursor without advancing the cursor
        """
        return self.source[self.current + 1] if not self.current + 1 > len(self.source) else None

    def _advance(self):
        """
        Return source code charater from the current cursor position
        and advance the cursor one character forward
        """
        if self._is_at_end():
            return None
        self.current += 1
        return self.source[self.current - 1]

    def _match(self, expected_char):
        if self._peek() != expected_char:
            return False
        self.current += 1
        return True
