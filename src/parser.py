from src.tokens import TokenType
from src.error_handler import ErrorHandler, ParseError

from src.ast_node_expression import Binary, Group, Literal, Unary, Variable, Assign

from src.ast_node_statement import VarStatement, ExpressionStatement, PrintStatement, \
    BlockStatement, IfStatement, WhileStatement, FunctionStatement, ReturnStatement, \
    ClassStatement
from src.parser_constants import EQUALITY_TOKENS, COMPARISON_TOKENS, TERM_TOKENS, FACTOR_TOKENS, \
    UNARY_TOKENS, LITERAL_TOKENS, IGNORED_TOKENS, GROUP_OPENING_TOKENS, GROUP_CLOSING_TOKENS, \
    STATEMENT_START_TOKENS, STATEMENT_END_TOKENS, IDENTIFIER_TOKENS, EQUALS_TOKENS, \
    VAR_STATEMENT_TOKENS, \
    PRINT_STATEMENT_TOKENS


class Parser:
    def __init__(self, tokens=None):
        self.tokens = [token for token in tokens if token.token_type not in IGNORED_TOKENS] if tokens else []
        self.index = 0
        self.error_handler = ErrorHandler()

    def parse(self):
        """
        Parse a list of tokens and return a list of statemeent
        Each statement is an abstract syntax tree
        Grammar:
        declaration -> VarStatement | statement
        statement -> ExpressionStatement | PrintStatement

        """
        statements = []
        try:
            while not self._end_of_code():
                statements.append(self._parse_declaring_statement())
        except ParseError as error:
            self.error_handler.report_error(error)  # TODO: refactor for the right place?
        return statements

    # PARSING STATEMENTS -----------------------------------------------------------------------------

    def _parse_declaring_statement(self):
        """
        Find next declaring statmemt and return its AST
        """
        try:
            if self._is_one_of_types(VAR_STATEMENT_TOKENS):
                return self._parse_var_statement()
            return self._parse_nondeclaring_statement()
        except ParseError:
            self._synchronize()
            # TODO: Raise exception again?

    def _parse_nondeclaring_statement(self):
        """
        Find next non-declaring statmemt and return its AST
        """
        if self._is_one_of_types(PRINT_STATEMENT_TOKENS):
            return self._parse_print_statement()

        return self._parse_expression_statement()

    def _parse_var_statement(self) -> VarStatement:
        name = self._consume_or_raise(IDENTIFIER_TOKENS, 'Expect variable name')
        initializer = self._expression() if self._is_one_of_types(EQUALS_TOKENS) else None
        self._consume_or_raise(STATEMENT_END_TOKENS, 'Expect statement terminator after value')
        return VarStatement(name, initializer)

    def _parse_expression_statement(self) -> ExpressionStatement:
        expression = self._expression()
        self._consume_or_raise(STATEMENT_END_TOKENS, 'Expect statement terminator after expression')
        return ExpressionStatement(expression)

    def _parse_print_statement(self) -> PrintStatement:
        print_value = self._expression()
        self._consume_or_raise(STATEMENT_END_TOKENS, 'Expect statement terminator after value')
        return PrintStatement(print_value)

    def _parse_block_statement(self) -> BlockStatement:
        pass

    def _parse_if_statement(self) -> IfStatement:
        pass

    def _parse_while_statement(self) -> WhileStatement:
        pass

    def _parse_function_statement(self) -> FunctionStatement:
        pass

    def _parse_return_statmeent(self) -> ReturnStatement:
        pass

    def _parse_class_statement(self) -> ClassStatement:
        pass

    # PARSING EXPRESSIONS -----------------------------------------------------------------------------

    def _expression(self):
        return self._assignment()

    def _assignment(self):
        # expression = self._equality()
        #
        # if self._is_one_of_types(EQUALS_TOKENS):
        #     equals = self._peek_prev()
        #     value = self._assignment()
        #
        #     if isinstance(expression, Variable):
        #         name = expression.name
        #         return Assign(name, value)
        #
        #     raise ParseError(token=equals, message='Invalid assignment target.')
        #
        # return expression

        expression = self._equality()
        if not self._is_one_of_types(EQUALS_TOKENS):
            return expression

        if not isinstance(expression, Variable):
            raise ParseError(token=self._peek_prev(), message='Invalid assignment target.')

        name = expression.name
        value = self._assignment()
        return Assign(name, value)

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
        A primary rule
        Grammar:
        primary -> literal | IDENTIFIER | "(" expression ")" ;
        literal -> INT | FLOAT | STRING | BOOL | "NULL" ;
        """
        if self._is_one_of_types(LITERAL_TOKENS):
            return Literal(self._peek_prev())

        if self._is_one_of_types(IDENTIFIER_TOKENS):
            return Variable(self._peek_prev())

        if self._is_one_of_types(GROUP_OPENING_TOKENS):
            expression = self._expression()
            self._consume_or_raise(GROUP_CLOSING_TOKENS, 'Expected closing parenthese')
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
            if self._peek_prev().token_type in STATEMENT_END_TOKENS:
                return
            if self._peek().token_type in STATEMENT_START_TOKENS:
                return
            self._next_token()
