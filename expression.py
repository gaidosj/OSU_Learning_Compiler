class Expression:
    class Binary():
        def __init__(self, leftOperand, operator, rightOperand):
            self.leftOperand = leftOperand
            self.operator = operator
            self.rightOperand = rightOperand

        def accept(self, visitor):
            visitor.visitBinary(self)

    class Group():
        def __init__(self, expression):
            self.expression = expression

        def accept(self, visitor):
            visitor.visitGroup(self)

    class Literal():
        def __init__(self, value):
            self.value = value

        def accept(self, visitor):
            visitor.visitLiteral(self)

    class Unary():
        def __init__(self, operator, operand):
            self.operator = operator
            self.operand = operand

        def accept(self, visitor):
            visitor.visitUnary(self)
