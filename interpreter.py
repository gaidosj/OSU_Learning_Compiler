from tokens import TokenType
from error_handler import ErrorHandler, InterpretError


class Interpreter:
    def __init__(self):
        self.error_handler = ErrorHandler()

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

    def visit_literal(self, literal):
        return literal.value.literal

    def visit_group(self, group):
        return self.evaluate(group.expression)

    def visit_unary(self, unary):
        operand = self.evaluate(unary.operand)

        if (unary.operator.token_type == TokenType.MINUS):
            return -operand
        elif (unary.operator.token_type == TokenType.NOT):
            return not self.is_truthy(operand)

    def visit_binary(self, binary):
        left = self.evaluate(binary.left_operand)
        right = self.evaluate(binary.right_operand)

        if (binary.operator.token_type == TokenType.ASTERISK):
            return left * right
        if (binary.operator.token_type == TokenType.DIV):
            return left / right
        if (binary.operator.token_type == TokenType.PLUS):
            return left + right
        if (binary.operator.token_type == TokenType.MINUS):
            return left - right
        if (binary.operator.token_type == TokenType.GT):
            return left > right
        if (binary.operator.token_type == TokenType.GTE):
            return left >= right
        if (binary.operator.token_type == TokenType.LT):
            return left < right
        if (binary.operator.token_type == TokenType.LTE):
            return left <= right
        if (binary.operator.token_type == TokenType.EQUALITY):
            return self.are_equal(left, right)
        if (binary.operator.token_type == TokenType.INEQUALITY):
            return not self.are_equal(left, right)
