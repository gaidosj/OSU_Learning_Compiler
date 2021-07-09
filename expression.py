class Expression:
    class Binary():
        def __init__(self, left_operand, operator, right_operand):
            self.left_operand = left_operand
            self.operator = operator
            self.right_operand = right_operand

        def accept(self, visitor):
            visitor.visit_binary(self)

    class Group():
        def __init__(self, expression):
            self.expression = expression

        def accept(self, visitor):
            visitor.visit_group(self)

    class Literal():
        def __init__(self, value):
            self.value = value

        def accept(self, visitor):
            visitor.visit_literal(self)

    class Unary():
        def __init__(self, operator, operand):
            self.operator = operator
            self.operand = operand

        def accept(self, visitor):
            visitor.visit_unary(self)
