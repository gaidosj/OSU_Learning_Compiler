from src.error_handler import ErrorHandler, InterpretError
from src.interpreter_runtime import RuntimeValue, RuntimeOperators


class Interpreter:
    def __init__(self):
        self.error_handler = ErrorHandler()

    def interpret(self, expression):
        try:
            return self.evaluate_expression(expression)
        except InterpretError as error:
            self.error_handler.report_error(error)

    def evaluate_expression(self, expression) -> RuntimeValue:
        return expression.accept(self)

    def visit_literal_expression(self, literal_expression) -> RuntimeValue:
        return RuntimeOperators.get_runtime_value_for_literal_token(
            token=literal_expression.value
        )

    def visit_group_expression(self, group_expression) -> RuntimeValue:
        return self.evaluate(group_expression.expression)

    def visit_unary_expression(self, unary_expression) -> RuntimeValue:
        return RuntimeOperators.get_runtime_value_for_unary_operator(
            operator=unary_expression.operator,
            operand=self.evaluate_expression(unary_expression.operand)
        )

    def visit_binary_expression(self, binary_expression) -> RuntimeValue:
        return RuntimeOperators.get_runtime_value_for_binary_operator(
            left=self.evaluate_expression(binary_expression.left_operand),
            operator=binary_expression.operator,
            right=self.evaluate_expression(binary_expression.right_operand)
        )
