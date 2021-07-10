from tokens import TokenType
from expression import Expression


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def expression(self):
        return self.equality()

    def equality(self):
        left_side = self.comparison()

        equality_types = [
            TokenType.EQUALITY,
            TokenType.INEQUALITY
        ]

        while self.is_one_of_types(equality_types):
            operator = self.peek_prev()
            right_side = self.comparison()
            left_side = Expression.Binary(left_side, operator, right_side)

        return left_side

    def comparison(self):
        left_side = self.term()

        comparison_types = [
            TokenType.LT,
            TokenType.LTE,
            TokenType.GT,
            TokenType.GTE
        ]

        while self.is_one_of_types(comparison_types):
            operator = self.peek_prev()
            right_side = self.term()
            left_side = Expression.Binary(left_side, operator, right_side)

        return self.term

    def term(self):
        left_side = self.factor()

        term_types = [
            TokenType.PLUS,
            TokenType.MINUS
        ]

        while self.is_one_of_types(term_types):
            operator = self.peek_prev()
            right_side = self.factor()
            left_side = Expression.Binary(left_side, operator, right_side)

        return left_side

    def factor(self):
        left_side = self.unary()

        factor_types = [
            TokenType.ASTERISK,
            TokenType.DIV
        ]

        while self.is_one_of_types(factor_types):
            operator = self.peek_prev()
            right_side = self.unary()
            left_side = Expression.Binary(left_side, operator, right_side)

        return left_side

    def unary(self):
        unary_types = [
            TokenType.NOT,
            TokenType.MINUS
        ]

        if self.is_one_of_types(unary_types):
            operator = self.peek_prev()
            right_side = self.unary()
            return Expression.Unary(operator, right_side)

        return self.primary()

    def primary(self):
        primary_types = [
            TokenType.INT,
            TokenType.IDENTIFIER
        ]

        if self.is_one_of_types(primary_types):
            return Expression.Literal(self.peek_prev().literal)

        if self.is_one_of_types(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.closeGroup(TokenType.RIGHT_PAREN)
            return Expression.Grouping(expr)

    def peek(self):
        return self.tokens[self.index]

    def peek_prev(self):
        return self.tokens[self.index - 1]

    def end_of_code(self):
        return self.peek().tokenType == TokenType.EOF

    def next_token(self):
        if not self.endOfCode():
            self.index += 1

        return self.peek_prev()

    def is_same_type(self, tokenType):
        return self.peek().tokenType == tokenType

    def is_one_of_types(self, tokenTypes):
        for tokenType in tokenTypes:
            if self.isSameType(tokenType):
                self.nextToken()
                return True
        return False

    def parse(self):
        try:
            return self.expression()
        except Exception:
            return None
