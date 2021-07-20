from src.tokens import TokenType
from src.error_handler import ErrorHandler, InterpretError


class Interpreter:
    def __init__(self):
        self.error_handler = ErrorHandler()
        self.binary_operators = {
            TokenType.MINUS: lambda left, right: left - right,
            TokenType.ASTERISK: lambda left, right: left * right,
            TokenType.DIV: lambda left, right: left // right,
            TokenType.PLUS: lambda left, right: left + right,
            TokenType.GTE: lambda left, right: left >= right,
            TokenType.GT: lambda left, right: left > right,
            TokenType.LTE: lambda left, right: left <= right,
            TokenType.LT: lambda left, right: left < right,
            TokenType.EQUALITY: lambda left, right: self.are_equal(
                left, right),
            TokenType.INEQUALITY: lambda left, right: not self.are_equal(
                left, right)
        }

    def interpret(self, expression):
        try:
            return self.evaluate(expression)
        except InterpretError as error:
            self.error_handler.report_error(error)

    def is_truthy(self, value):
        if value is None or value == 0:
            return False
        return True

    def are_equal(self, one, other):
        return one == other

    def evaluate(self, expression):
        return expression.accept(self)

    def visit_literal_expression(self, literal):
        return literal.value.literal

    def visit_group_expression(self, group):
        return self.evaluate(group.expression)

    def visit_unary_expression(self, unary):
        operand = self.evaluate(unary.operand)

        if (unary.operator.token_type == TokenType.MINUS):
            return -operand
        elif (unary.operator.token_type == TokenType.NOT):
            return not self.is_truthy(operand)

    def visit_binary_expression(self, binary):
        left = self.evaluate(binary.left_operand)
        right = self.evaluate(binary.right_operand)

        return self.binary_operators[binary.operator.token_type](left, right)
