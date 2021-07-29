from src.tokens import TokenOsu
from src.ast_node_expression import ParserExpression, Variable
from src.abstract_syntax_tree import AbstractSyntaxTree


class ParserStatement:
    def __eq__(self, other):
        # TODO: Do we need deep compare here?
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __str__(self):
        return str(AbstractSyntaxTree(self))


class VarStatement(ParserStatement):
    """
    Create a binding between variable name and a value
    """
    def __init__(self, name: TokenOsu, initializer: ParserExpression):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_var_statement(self)


class ExpressionStatement(ParserStatement):
    def __init__(self, expression: ParserExpression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression_statement(self)


class PrintStatement(ParserStatement):
    def __init__(self, expression: ParserExpression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_print_statement(self)


class BlockStatement(ParserStatement):
    def __init__(self, statements: [ParserStatement]):
        self.statements = statements.copy()  # TODO need this copy or mutable is OK?

    def accept(self, visitor):
        return visitor.visit_block_statement(self)


class IfStatement(ParserStatement):
    def __init__(self, condition: ParserExpression, then_branch: ParserStatement, else_branch: ParserStatement):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visit_if_statement(self)


class WhileStatement(ParserStatement):
    def __init__(self, condition: ParserExpression, body: ParserStatement):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while_statement(self)


class FunctionStatement(ParserStatement):
    def __init__(self, name: TokenOsu, parameters: [TokenOsu], body: [ParserStatement]):
        self.name = name
        self.parameters = parameters.copy()  # TODO: Need copy?
        self.body = body

    def accept(self, visitor):
        return visitor.visit_function_statement(self)


class ReturnStatement(ParserStatement):
    def __init__(self, keyword: TokenOsu, value: ParserExpression):
        self.keyword = keyword
        self.value = value

    def accept(self, visitor):
        return visitor.visit_return_statement(self)


class ClassStatement(ParserStatement):
    def __init__(self, name: TokenOsu, super_class: Variable, methods: [FunctionStatement]):
        self.name = name
        self.super_class = super_class
        self.methods = methods.copy()  # TODO: copy() or mutable?

    def accept(self, visitor):
        return visitor.visit_class_statement(self)
