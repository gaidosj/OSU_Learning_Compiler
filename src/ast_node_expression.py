from src.tokens import TokenOsu
from src.abstract_syntax_tree import AbstractSyntaxTree


class ParserExpression:
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __str__(self):
        return str(AbstractSyntaxTree(self))


class Binary(ParserExpression):
    def __init__(self, left_operand: ParserExpression, operator: TokenOsu, right_operand: ParserExpression):
        self.left_operand = left_operand
        self.operator = operator
        self.right_operand = right_operand

    def accept(self, visitor):
        return visitor.visit_binary_expression(self)


class Group(ParserExpression):
    def __init__(self, expression: ParserExpression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_group_expression(self)


class Literal(ParserExpression):
    def __init__(self, token: TokenOsu):
        self.value = token

    def accept(self, visitor):
        return visitor.visit_literal_expression(self)


class Unary(ParserExpression):
    def __init__(self, operator: TokenOsu, operand: ParserExpression):
        self.operator = operator
        self.operand = operand

    def accept(self, visitor):
        return visitor.visit_unary_expression(self)


class Assign(ParserExpression):
    def __init__(self, name: TokenOsu, value: ParserExpression):
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assign_expression(self)


class Variable(ParserExpression):
    def __init__(self, name: TokenOsu):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable_expression(self)


class Call(ParserExpression):
    def __init__(self, callee, paren, arguments):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visit_call_expression(self)


class Get(ParserExpression):
    def __init__(self, object: ParserExpression, name: TokenOsu):
        self.object = object
        self.name = name

    def accept(self, visitor):
        return visitor.visit_get_expression(self)


class This(ParserExpression):
    def __init__(self, keyword: TokenOsu):
        self.keyword = keyword

    def accept(self, visitor):
        return visitor.visit_this_expression(self)


class Set(ParserExpression):
    def __init__(self, object: ParserExpression, name: TokenOsu, value: ParserExpression):
        self.object = object
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_set_expression(self)


class Super(ParserExpression):
    def __init__(self, keyword: TokenOsu, method: TokenOsu):
        self.keyword = keyword
        self.method = method

    def accept(self, visitor):
        return visitor.visit_super_expression(self)
