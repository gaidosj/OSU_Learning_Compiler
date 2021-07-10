from tokens import TokenType
from expression import Expression
from error_handler import ErrorHandler
from error_handler import ParseError


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def parse(self):
        try:
            return self._expression()
        except ParseError as error:
            ErrorHandler.report_error(error)
            return None

    def _expression(self):
        return self._equality()

    def _equality(self):
        left_side = self._comparison()

        equality_types = [
            TokenType.EQUALITY,
            TokenType.INEQUALITY
        ]

        while self._is_one_of_types(equality_types):
            operator = self._peek_prev()
            right_side = self._comparison()
            left_side = Expression.Binary(left_side, operator, right_side)

        return left_side

    def _comparison(self):
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
            left_side = Expression.Binary(left_side, operator, right_side)

        return self.term

    def _term(self):
        left_side = self._factor()

        term_types = [
            TokenType.PLUS,
            TokenType.MINUS
        ]

        while self._is_one_of_types(term_types):
            operator = self._peek_prev()
            right_side = self._factor()
            left_side = Expression.Binary(left_side, operator, right_side)

        return left_side

    def _factor(self):
        left_side = self._unary()

        factor_types = [
            TokenType.ASTERISK,
            TokenType.DIV
        ]

        while self._is_one_of_types(factor_types):
            operator = self._peek_prev()
            right_side = self._unary()
            left_side = Expression.Binary(left_side, operator, right_side)

        return left_side

    def _unary(self):
        unary_types = [
            TokenType.NOT,
            TokenType.MINUS
        ]

        if self._is_one_of_types(unary_types):
            operator = self._peek_prev()
            right_side = self._unary()
            return Expression._unary(operator, right_side)

        return self._primary()

    def _primary(self):
        primary_types = [
            TokenType.INT,
            TokenType.IDENTIFIER
        ]

        if self._is_one_of_types(primary_types):
            return Expression.Literal(self._peek_prev().literal)

        if self._is_one_of_types(TokenType.LEFT_PAREN):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, 'Expected closing paren ")"')
            return Expression.Grouping(expr)

        raise ParseError(self._peek(), 'Expected start of expression')

    def _peek(self):
        return self.tokens[self.index]

    def _peek_prev(self):
        return self.tokens[self.index - 1]

    def _end_of_code(self):
        return self._peek().token_type == TokenType.EOF

    def _next_token(self):
        if not self.endOfCode():
            self.index += 1

        return self._peek_prev()

    def _is_same_type(self, token_type):
        return self._peek().token_type == token_type

    def _is_one_of_types(self, token_type):
        for tokenType in token_type:
            if self._is_same_type(token_type):
                self._next_token()
                return True
        return False

    def _consume(self, token_type, message):
        if (self._is_same_type(token_type)):
            return self._next_token()

        raise ParseError(self._peek(), message)

    def _synchronize(self):
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
