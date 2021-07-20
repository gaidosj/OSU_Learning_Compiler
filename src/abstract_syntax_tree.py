class AbstractSyntaxTree:
    def __init__(self, root):
        self.root = root

    def __str__(self):
        return self.root.accept(self)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def visit_binary_expression(self, binary_expression):
        return '({} {} {})'.format(
            binary_expression.left_operand.accept(self),
            binary_expression.operator.lexeme,
            binary_expression.right_operand.accept(self),
        )

    def visit_group_expression(self, group_expression):
        return 'Paren({})'.format(
            group_expression.expression.accept(self),
        )

    def visit_literal_expression(self, literal_expression):
        return '{}'.format(
            literal_expression.value.literal,
        )

    def visit_unary_expression(self, unary_expression):
        return '({}{})'.format(
            unary_expression.operator.lexeme,
            unary_expression.operand.accept(self),
        )

    def visit_assign_expression(self, assign_expression):
        return '({} = {})'.format(
            assign_expression.name.literal,
            assign_expression.value.accept(self),
        )

    def visit_variable_expression(self, variable_expression):
        return '{}'.format(
            variable_expression.name.literal,
        )

    def visit_call_expression(self, call_expression):
        pass

    def visit_get_expression(self, get_expression):
        pass

    def visit_this_exression(self, this_expression):
        pass

    def visit_set_expression(self, set_expression):
        pass

    def visit_super_expression(self, super_expression):
        pass

    def visit_var_statement(self, var_statement):
        pass

    def visit_expression_statement(self, expression_statement):
        pass

    def visit_print_statement(self, print_statement):
        pass

    def visit_block_statement(self, block_statement):
        pass

    def visit_if_statement(self, if_statement):
        pass

    def visit_while_statement(self, while_statement):
        pass

    def visit_function_statement(self, function_statement):
        pass

    def visit_return_statement(self, return_statement):
        pass

    def visit_class_stateement(self, class_statement):
        pass
