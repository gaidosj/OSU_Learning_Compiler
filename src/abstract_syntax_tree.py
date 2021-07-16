class AbstractSyntaxTree:
    def __init__(self, root):
        self.root = root

    def __str__(self):
        return self.root.accept(self)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def visit_binary(self, binary):
        return ''.join(['(', ' '.join([
            binary.left_operand.accept(self),
            str(binary.operator.literal),
            binary.right_operand.accept(self),
        ]), ')'])

    def visit_group(self, group):
        return ''.join(['Paren(', group.expression.accept(self), ')'])

    def visit_literal(self, literal):
        return str(literal.value.literal)

    def visit_unary(self, unary):
        return ''.join([
            '(', str(unary.operator.literal), unary.operand.accept(self), ')'])
