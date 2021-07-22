from src.error_handler import ErrorHandler, InterpretError
from src.interpreter_runtime import RuntimeValue, RuntimeOperators


class Interpreter:
    def __init__(self):
        self.error_handler = ErrorHandler()

    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute_statement(statement)
        except InterpretError as error:
            self.error_handler.report_error(error)

    def execute_statement(self, statement) -> None:
        statement.accept(self)

    def evaluate_expression(self, expression) -> RuntimeValue:
        return expression.accept(self)

    # VISITOR INTERFACE FOR STATEMENTS ----------------------------------------------

    def visit_var_statement(self, var_statement) -> None:
        pass

    def visit_expression_statement(self, expression_statement) -> None:
        self.evaluate_expression(expression_statement.expression)

    def visit_print_statement(self, print_statement) -> None:
        print_value = self.evaluate_expression(print_statement.expression)
        print(print_value.value)

    def visit_block_statement(self, block_statement) -> None:
        pass

    def visit_if_statement(self, if_statement) -> None:
        pass

    def visit_while_statement(self, while_statement) -> None:
        pass

    def visit_function_statement(self, function_statement) -> None:
        pass

    def visit_return_statement(self, return_statement) -> None:
        pass

    def visit_class_statement(self, class_statement) -> None:
        pass

    # VISITOR INTERFACE FOR EXPRESSIONS ---------------------------------------------

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
