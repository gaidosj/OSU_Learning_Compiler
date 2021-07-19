class AbstractSyntaxTree:
    def __init__(self, root):
        self.root = root

    def __str__(self):
        return self.root.accept(self)

    def __eq__(self, other):
        if isinstance(other, self.__class__):           # TODO: does this do deep comparison?
            return self.__dict__ == other.__dict__
        else:
            return False

    def visit_binary_expression(self, binary):
        return ''.join(['(', ' '.join([
            binary.left_operand.accept(self),
            str(binary.operator.literal),
            binary.right_operand.accept(self),
        ]), ')'])

    def visit_group_expression(self, group):
        return ''.join(['Paren(', group.expression.accept(self), ')'])

    def visit_literal_expression(self, literal):
        return str(literal.value.literal)

    def visit_unary_expression(self, unary):
        return ''.join([
            '(', str(unary.operator.literal), unary.operand.accept(self), ')'])

    def visit_assign_expression(self, assign_expression):
        pass

    def visit_variable_expression(self, variable_expression):
        pass

    def visit_logical_binary_expression(self, logical_binary_expression):
        pass

    def visit_logical_unary_expression(self, logical_unary_expression):
        pass

    def visit_var_statement(self, var_statement):
        pass

    def visit_expression_statement(self, expression_statement):
        pass

    def visit_block_statement(self, block_statement):
        pass
