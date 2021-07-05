from olc_token import OLCToken
from expression import Expression


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def expression(self):
        return self.equality()

    def equality(self):
        leftSide = self.comparison()

        equalityTypes = [
            OLCToken.Types.EQUALITY,
            OLCToken.Types.INEQUALITY
        ]

        while self.isOneOfTypes(equalityTypes):
            operator = self.peekPrev()
            rightSide = self.comparison()
            leftSide = Expression.Binary(leftSide, operator, rightSide)

        return leftSide

    def comparison(self):
        leftSide = self.term()

        comparisonTypes = [
            OLCToken.Types.GREATER_THAN,
            OLCToken.Types.GREATER_EQUAL,
            OLCToken.Types.LESS_THAN,
            OLCToken.Types.LESS_EQUAL
        ]

        while self.isOneOfTypes(comparisonTypes):
            operator = self.peekPrev()
            rightSide = self.term()
            leftSide = Expression.Binary(leftSide, operator, rightSide)

        return self.term

    def term(self):
        leftSide = self.factor()

        termTypes = [
            OLCToken.Types.ADDITION,
            OLCToken.Types.SUBTRACTION
        ]

        while self.isOneOfTypes(termTypes):
            operator = self.peekPrev()
            rightSide = self.factor()
            leftSide = Expression.Binary(leftSide, operator, rightSide)

        return leftSide

    def factor(self):
        leftSide = self.unary()

        factorTypes = [
            OLCToken.Types.Multiplication,
            OLCToken.Types.Division
        ]

        while self.isOneOfTypes(factorTypes):
            operator = self.peekPrev()
            rightSide = self.unary()
            leftSide = Expression.Binary(leftSide, operator, rightSide)

        return leftSide

    def unary(self):
        unaryTypes = [
            OLCToken.Types.NOT,
            OLCToken.Types.SUBTRACTION
        ]

        if self.isOneOfTypes(unaryTypes):
            operator = self.peekPrev()
            rightSide = self.unary()
            return Expression.Unary(operator, rightSide)

        return self.primary()

    def primary(self):
        primaryTypes = [
            OLCToken.Types.INTEGER,
            OLCToken.Types.IDENTIFIER
        ]

        if self.isOneOfTypes(primaryTypes):
            return Expression.Literal(self.peekPrev().literal)

        if self.isOneOfTypes(OLCToken.Types.LEFT_PAREN):
            expr = self.expression()
            self.closeGroup(OLCToken.Types.RIGHT_PAREN)
            return Expression.Grouping(expr)

    def peek(self):
        return self.tokens[self.index]

    def peekPrev(self):
        return self.tokens[self.index - 1]

    def endOfCode(self):
        return self.peek().tokenType == OLCToken.OLCToken.Types.EOF

    def nextToken(self):
        if not self.endOfCode():
            self.index += 1

        return self.peekPrev()

    def isSameType(self, tokenType):
        return self.peek().tokenType == tokenType

    def isOneOfTypes(self, tokenTypes):
        for tokenType in tokenTypes:
            if self.isSameType(tokenType):
                self.nextToken()
                return True
        return False

    def parse(self):
        try:
            return self.expression()
        except Exception:
            return None
