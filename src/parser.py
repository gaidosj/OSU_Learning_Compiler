from src.tokens import TokenType
from src.error_handler import ErrorHandler, ParseError

from src.ast_node_expression import Binary, Group, Literal, Unary

from src.ast_node_statement import VarStatement, ExpressionStatement, PrintStatement, \
    BlockStatement, IfStatement, WhileStatement, FunctionStatement, ReturnStatement, \
    ClassStatement
from src.parser_constants import EQUALITY_TOKENS, COMPARISON_TOKENS, TERM_TOKENS, FACTOR_TOKENS, \
    UNARY_TOKENS, LITERAL_TOKENS, IGNORED_TOKENS, GROUP_OPENING, GROUP_CLOSING, \
    STATEMENT_START_TOKENS, STATEMENT_END_TOKENS, \
    PRINT_STATEMENT_TOKENS


class Parser:
    def __init__(self, tokens=None):
        self.tokens = [token for token in tokens if token not in IGNORED_TOKENS] if tokens else []
        self.index = 0
        self.error_handler = ErrorHandler()

    def parse(self):
        """
        Parses a list of tokens and returns an abstract syntax tree
        """
        statements = []
        while not self._end_of_code():
            statements.append(self._statement())

        return statements

        # if self.tokens:
        #     try:
        #         self.index = 0
        #         return AbstractSyntaxTree(self._expression())
        #     except ParseError as error:
        #         self.error_handler.report_error(error)

    # STATEMENTS -----------------------------------------------------------------------------------

    def _statement(self):
        """
        Find next statmemt and return the AST of it
        """
        if self._is_one_of_types(PRINT_STATEMENT_TOKENS):
            return self._print_statement()

        return self._expression_statement()





    def _print_statement(self) -> PrintStatement:
        print_value = self._expression()
        self._consume_or_raise(STATEMENT_END_TOKENS, 'Expect ; after value')
        return PrintStatement(print_value)

    def _expression_statement(self) -> ExpressionStatement:
        expression = self._expression()
        self._consume_or_raise(STATEMENT_END_TOKENS, 'Expect ; after expression')
        return ExpressionStatement(expression)






    # EXPRESSIONS -----------------------------------------------------------------------------------

    def _expression(self):
        """
        Any type of expression in the language
        """
        return self._equality()

    def _equality(self):
        """
        Checks for equality between two operands
        Grammar: equality → comparison ( ( "!=" | "==" ) comparison )* ;
        """
        left_side = self._comparison()
        while self._is_one_of_types(EQUALITY_TOKENS):
            operator = self._peek_prev()
            right_side = self._comparison()
            left_side = Binary(left_side, operator, right_side)
        return left_side

    def _comparison(self):
        """
        Compares two operands
        Grammar: comparison → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
        """
        left_side = self._term()
        while self._is_one_of_types(COMPARISON_TOKENS):
            operator = self._peek_prev()
            right_side = self._term()
            left_side = Binary(left_side, operator, right_side)
        return left_side

    def _term(self):
        """
        Adds or subtracts operands
        """
        left_side = self._factor()
        while self._is_one_of_types(TERM_TOKENS):
            operator = self._peek_prev()
            right_side = self._factor()
            left_side = Binary(left_side, operator, right_side)
        return left_side

    def _factor(self):
        """
        Multiplies or divides operands
        """
        left_side = self._unary()
        while self._is_one_of_types(FACTOR_TOKENS):
            operator = self._peek_prev()
            right_side = self._unary()
            left_side = Binary(left_side, operator, right_side)
        return left_side

    def _unary(self):
        """
        Acts on a single operand
        Grammar: unary → ( "!" | "-" ) unary | primary ;
        """
        if self._is_one_of_types(UNARY_TOKENS):
            operator = self._peek_prev()
            right_side = self._unary()
            return Unary(operator, right_side)
        return self._primary()

    def _primary(self):
        """
        A literal type
        Grammar: primary → INT | FLOAT | STRING | BOOL | "NULL" | "(" expression ")" ;
        """
        if self._is_one_of_types(LITERAL_TOKENS):
            return Literal(self._peek_prev())

        if self._is_one_of_types(GROUP_OPENING):
            expression = self._expression()
            self._consume_or_raise(GROUP_CLOSING, 'Expected closing parenthese')
            return Group(expression)

        raise ParseError(self._peek(), 'Expected start of expression')

    # HELPER METHODS -----------------------------------------------------------------------------------

    def _peek(self):
        """
        Look at the next token
        """
        return self.tokens[self.index] if not self._out_of_bounds() else None

    def _peek_prev(self):
        """
        Look at the current token
        """
        return self.tokens[self.index - 1] if self.index > 0 else None

    def _out_of_bounds(self):
        """
        Return true if index is out of bounds for the tokens array
        """
        return self.index >= len(self.tokens)

    def _end_of_code(self):
        """
        Return true if the end of the file has been reached
        """
        # return self.index > len(self.tokens)  # TODO: Refactor? How different from end_of_code?
        if not self._out_of_bounds():
            if self._peek().token_type == TokenType.EOF:
                return True
            return False
        return True

    def _next_token(self):
        """
        Return the next token and advance
        """
        self.index += not self._end_of_code()
        return self._peek_prev()

    def _is_same_type(self, token_type):
        """
        Checks whether next token is of given type
        """
        return not self._out_of_bounds() and self._peek().token_type == token_type

    def _is_one_of_types(self, token_types):
        """
        Advances the token pointer if token is one of given types
        """
        if self._peek() and self._peek().token_type in token_types:
            self._next_token()
            return True
        return False

    def _consume_or_raise(self, token_types, exception_description):
        """
        Consumes the expected token or throws an error
        """
        if any([self._is_same_type(token_type) for token_type in token_types]):
            return self._next_token()
        raise ParseError(token=self._peek(), message=exception_description)

    def _synchronize(self):
        """
        Panic mode recovery - find the likely start of the next statement
        """
        self._next_token()

        while not self._end_of_code():
            if self._peek_prev().type in STATEMENT_END_TOKENS or self._peek().type in STATEMENT_START_TOKENS:
                return
            self._next_token()
