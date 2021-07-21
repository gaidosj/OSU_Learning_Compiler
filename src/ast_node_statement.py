from src.tokens import TokenOsu
from src.ast_node_expression import ParserExpression, Variable


class ParserStatement:
    def __eq__(self, other):
        # TODO: Do we need deep compare here?
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


class Var(ParserStatement):
    def __init__(self, name: TokenOsu, initializer: ParserExpression):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_var_statement(self)


class Expression(ParserStatement):
    def __init__(self, expression: ParserExpression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression_statement(self)


class Print(ParserStatement):
    def __init__(self, expression: ParserExpression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_print_statement(self)


class Block(ParserStatement):
    def __init__(self, statements: [ParserStatement]):
        self.statements = statements.copy()  # TODO need this copy or mutable is OK?

    def accept(self, visitor):
        return visitor.visit_block_statement(self)


class If(ParserStatement):
    def __init__(self, condition: ParserExpression, then_branch: ParserStatement, else_branch: ParserStatement):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visit_if_statement(self)


class While(ParserStatement):
    def __init__(self, condition: ParserExpression, body: ParserStatement):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while_statement(self)


class Function(ParserStatement):
    def __init__(self, name: TokenOsu, parameters: [TokenOsu], body: [ParserStatement]):
        self.name = name
        self.parameters = parameters.copy()  # TODO: Need copy?
        self.body = body.copy()  # TODO: Need list of single stm?

    def accept(self, visitor):
        return visitor.visit_function_statement(self)


class Return(ParserStatement):
    def __init__(self, keyword: TokenOsu, value: ParserExpression):
        self.keyword = keyword
        self.value = value

    def accept(self, visitor):
        return visitor.visit_return_statement(self)


class Class(ParserStatement):
    def __init__(self, name: TokenOsu, super_class: Variable, methods: [Function]):
        self.name = name
        self.super_class = super_class
        self.methods = methods.copy()  # TODO: copy() or mutable?

    def accept(self, visitor):
        return visitor.visit_class_statement(self)
