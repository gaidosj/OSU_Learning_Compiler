from src.constants import AppType
from src.error_handler import ErrorHandler, InterpretError
from src.function import Function
from src.interpreter_runtime import RuntimeValue, RuntimeDataType, RuntimeOperators, Environment
from src.logger import Logger as log


class Interpreter:
    def __init__(self):
        self.environment = Environment()
        self.error_handler = ErrorHandler()

    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute_statement(statement)
        except InterpretError as error:
            self.error_handler.report_error(error)

    def execute_block(self, statements, environment):
        old_environment = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute_statement(statement)
        finally:
            self.environment = old_environment

    def execute_statement(self, statement) -> None:
        # from src.abstract_syntax_tree import AbstractSyntaxTree
        # print("EXECUTING STATEMENT:", AbstractSyntaxTree(statement) if statement else 'NONE')
        statement.accept(self)

    def evaluate_expression(self, expression) -> RuntimeValue:
        # print("   EVALUATING EXPRESSION:", AbstractSyntaxTree(expression) if expression else 'NONE')
        return expression.accept(self)

    # VISITOR INTERFACE FOR STATEMENTS ----------------------------------------------

    def visit_var_statement(self, var_statement) -> None:
        log.info(AppType.INTERPRETER, f'visit_var_statement: {var_statement}')
        if var_statement.initializer:
            value = self.evaluate_expression(var_statement.initializer)
        else:
            value = RuntimeValue(value=None, data_type=RuntimeDataType.NULL)
        self.environment.define(name=var_statement.name.lexeme, value=value)

    def visit_expression_statement(self, expression_statement) -> None:
        log.info(AppType.INTERPRETER, f'visit_expression_statement: {expression_statement}')
        self.evaluate_expression(expression_statement.expression)

    def visit_print_statement(self, print_statement) -> None:
        log.info(AppType.INTERPRETER, f'visit_print_statement: {print_statement}')
        print_value = self.evaluate_expression(print_statement.expression)
        print(print_value.value)

    def visit_block_statement(self, block_statement) -> None:
        log.info(AppType.INTERPRETER, f'visit_block_statement: {block_statement}')
        self.execute_block(block_statement.statements, Environment(enclosing_environment=self.environment))
        log.info(AppType.INTERPRETER, f'finished visit_block_statement {block_statement}')

    def visit_if_statement(self, if_statement) -> None:
        log.info(AppType.INTERPRETER, f'visit_if_statement: {if_statement}')
        if self.evaluate_expression(if_statement.condition).is_truthy():
            self.execute_statement(if_statement.then_branch)
        elif if_statement.else_branch:
            self.execute_statement(if_statement.else_branch)

    def visit_while_statement(self, while_statement) -> None:
        log.info(AppType.INTERPRETER, f'visit_while_statement: {while_statement}')
        while self.evaluate_expression(while_statement.condition).is_truthy():
            self.execute_statement(while_statement.body)

    def visit_function_statement(self, function_statement) -> None:
        log.info(AppType.INTERPRETER, f'visit_function_statement: {function_statement}')
        pass

    def visit_return_statement(self, return_statement) -> None:
        log.info(AppType.INTERPRETER, f'visit_return_statement: {return_statement}')
        pass

    def visit_class_statement(self, class_statement) -> None:
        log.info(AppType.INTERPRETER, f'visit_class_statement: {class_statement}')
        pass

    # VISITOR INTERFACE FOR EXPRESSIONS ---------------------------------------------

    def visit_binary_expression(self, binary_expression) -> RuntimeValue:
        return RuntimeOperators.get_runtime_value_for_binary_operator(
            left=self.evaluate_expression(binary_expression.left_operand),
            operator=binary_expression.operator,
            right=self.evaluate_expression(binary_expression.right_operand)
        )

    def visit_group_expression(self, group_expression) -> RuntimeValue:
        return self.evaluate_expression(group_expression.expression)

    def visit_literal_expression(self, literal_expression) -> RuntimeValue:
        return RuntimeOperators.get_runtime_value_for_literal_token(
            token=literal_expression.value
        )

    def visit_unary_expression(self, unary_expression) -> RuntimeValue:
        return RuntimeOperators.get_runtime_value_for_unary_operator(
            operator=unary_expression.operator,
            operand=self.evaluate_expression(unary_expression.operand)
        )

    def visit_assign_expression(self, assign_expression) -> RuntimeValue:
        value = self.evaluate_expression(assign_expression.value)
        self.environment.assign(assign_expression.name, value)
        return value

    def visit_variable_expression(self, variable_expression) -> RuntimeValue:
        return self.environment.get(variable_expression.name)

    def visit_call_expression(self, call_expression) -> RuntimeValue:
        callee = self.evaluate_expression(call_expression.callee)
        arguments = [self.evaluate_expression(arg) for arg in call_expression.arguments]
        function = Function(callee)
        return function.call(self, arguments)

    def visit_get_expression(self, get_expression) -> RuntimeValue:
        pass

    def visit_this_expression(self, this_expression) -> RuntimeValue:
        pass

    def visit_set_expression(self, set_expression) -> RuntimeValue:
        pass

    def visit_super_expression(self, super_expression) -> RuntimeValue:
        pass
