from src.tokens import TokenOsu
from src.parser_expression import ParserExpression


class ParserStatement:
    def __eq__(self, other):
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
    pass


class Block(ParserStatement):
    def __init__(self, statements: [ParserStatement]):
        self.statements = statements.copy()  # TODO need this copy or mutable is OK?

    def accept(self, visitor):
        return visitor.visit_block_statement(self)


class If(ParserStatement):
    pass


class While(ParserStatement):
    pass


class Function(ParserStatement):
    pass


class Return(ParserStatement):
    pass


class Class(ParserStatement):
    pass
