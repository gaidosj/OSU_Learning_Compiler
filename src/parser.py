from src.tokens import TokenType
from src.parser_expression import Binary, Group, Literal, Unary
from src.error_handler import ErrorHandler, ParseError
from src.abstract_syntax_tree import AbstractSyntaxTree


class Parser:
    def __init__(self, tokens=None):
        self.tokens = tokens.copy() if tokens else []
        self.index = 0
        self.error_handler = ErrorHandler()

    def parse(self):
        """
        Parses a list of tokens and returns an abstract syntax tree
        """
        if not self.tokens:
            return

        try:
            self.index = 0
            return AbstractSyntaxTree(self._expression())
        except ParseError as error:
            self.error_handler.report_error(error)

    def _expression(self):
        """Any type of expression in the language"""
        return self._equality()

    def _equality(self):
        """Checks for equality between two operands"""
        left_side = self._comparison()

        equality_types = [
            TokenType.EQUALITY,
            TokenType.INEQUALITY
        ]

        while self._is_one_of_types(equality_types):
            operator = self._peek_prev()
            right_side = self._comparison()
            left_side = Binary(left_side, operator, right_side)

        return left_side

    def _comparison(self):
        """Compares two operands"""
        left_side = self._term()

        comparison_types = [
            TokenType.LT,
            TokenType.LTE,
            TokenType.GT,
            TokenType.GTE
        ]

        while self._is_one_of_types(comparison_types):
            operator = self._peek_prev()
            right_side = self._term()
            left_side = Binary(left_side, operator, right_side)

        return left_side

    def _term(self):
        """Adds or subtracts operands"""
        left_side = self._factor()

        term_types = [
            TokenType.PLUS,
            TokenType.MINUS
        ]

        while self._is_one_of_types(term_types):
            operator = self._peek_prev()
            right_side = self._factor()
            left_side = Binary(left_side, operator, right_side)

        return left_side

    def _factor(self):
        """Multiplies or divides operands"""
        left_side = self._unary()

        factor_types = [
            TokenType.ASTERISK,
            TokenType.DIV
        ]

        while self._is_one_of_types(factor_types):
            operator = self._peek_prev()
            right_side = self._unary()
            left_side = Binary(left_side, operator, right_side)

        return left_side

    def _unary(self):
        """Acts on a single operand"""
        unary_types = [
            TokenType.NOT,
            TokenType.MINUS
        ]

        if self._is_one_of_types(unary_types):
            operator = self._peek_prev()
            right_side = self._unary()
            return Unary(operator, right_side)

        return self._primary()

    def _primary(self):
        """A literal type"""
        primary_types = [
            TokenType.INT,
            TokenType.IDENTIFIER
        ]

        if self._is_one_of_types(primary_types):
            return Literal(self._peek_prev())

        closing_parens = [TokenType.LEFT_PAREN]

        if self._is_one_of_types(closing_parens):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, 'Expected closing paren ")"')
            return Group(expr)

        raise ParseError(self._peek(), 'Expected start of expression')

    def _peek(self):
        """Look at the next token"""
        if not self._out_of_bounds():
            return self.tokens[self.index]
        return None

    def _peek_prev(self):
        """Look at the current token"""
        return self.tokens[self.index - 1]

    def _out_of_bounds(self):
        """Return true if index is out of bounds for the tokens array"""
        return self.index >= len(self.tokens)

    def _end_of_code(self):
        """Return true if the end of the file has been reached"""
        if not self._out_of_bounds():
            if self._peek().token_type == TokenType.EOF:
                return True
            return False
        return True

    def _next_token(self):
        """Return the next token and advance"""
        if not self._end_of_code():
            self.index += 1

        return self._peek_prev()

    def _is_same_type(self, token_type):
        """Checks whether next token is of given type"""
        if not self._out_of_bounds():
            return self._peek().token_type == token_type
        return False

    def _is_one_of_types(self, token_types):
        """Advances the token pointer if token is one of given types"""
        for token_type in token_types:
            if self._is_same_type(token_type):
                self._next_token()
                return True
        return False

    def _consume(self, token_type, message):
        """Consumes the expected token or throws an error"""
        if (self._is_same_type(token_type)):
            return self._next_token()

        raise ParseError(self._peek(), message)

    def _synchronize(self):
        """Finds the next valid token that can start an expression"""
        self._next_token()

        while not self._end_of_code():
            if (self._peek_prev().type == TokenType.SEMICOLON):
                return

            starting_types = [
                TokenType.CLASS,
                TokenType.FUNCTION,
                TokenType.VAR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN
            ]

            if self._peek().type in starting_types:
                return

            self._next_token()
