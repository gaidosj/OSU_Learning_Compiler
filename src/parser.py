from src.constants import AppType
from src.logger import Logger as log
from src.tokens import TokenType
from src.error_handler import ErrorHandler, ParseError

from src.ast_node_expression import Binary, Group, Literal, Unary, Variable, Assign, Call

from src.ast_node_statement import VarStatement, ExpressionStatement, PrintStatement, \
    BlockStatement, IfStatement, WhileStatement, FunctionStatement, ReturnStatement, \
    ClassStatement
from src.parser_constants import EQUALITY_TOKENS, COMPARISON_TOKENS, TERM_TOKENS, FACTOR_TOKENS, \
    UNARY_TOKENS, LITERAL_TOKENS, IGNORED_TOKENS, GROUP_OPENING_TOKENS, GROUP_CLOSING_TOKENS, \
    STATEMENT_START_TOKENS, STATEMENT_END_TOKENS, IDENTIFIER_TOKENS, EQUALS_TOKENS, \
    BLOCK_OPENING_TOKENS, BLOCK_CLOSING_TOKENS, VAR_STATEMENT_TOKENS, FUNCTION_STATEMENT_TOKENS, DELIMITER_TOKENS


class Parser:
    def __init__(self, tokens=None):
        self.upload_tokens(tokens)

    def upload_tokens(self, tokens):
        self.tokens = [token for token in tokens if token.token_type not in IGNORED_TOKENS] if tokens else []
        # TODO: May need deep copy to avoid side effects
        self.index = 0
        self.error_handler = ErrorHandler()
        self.statements = []

    def get_statements(self):
        return self.statements

    def parse(self, tokens=None):
        """
        Parse a list of tokens and return a list of statement
        Each statement is an abstract syntax tree
        """
        if tokens:
            self.upload_tokens(tokens)

        source_tokens = ' '.join([str(token) for token in self.tokens])
        log.info(AppType.PARSER, f'Tokens: {source_tokens}')

        self.statements = []
        while not self._end_of_code():
            self.statements.append(self._parse_statement())
        return self.statements

    # PARSING STATEMENTS -----------------------------------------------------------------------------

    def _parse_statement(self):
        try:
            return self._parse_declaring_statement()
        except ParseError as error:
            self.error_handler.add_error(error)
            self._synchronize()

    def _parse_declaring_statement(self):
        """
        Find next declaring statememt and return its AST
        (VAR, FUNCTION and CLASS are declaring statements)
        """
        if self._is_one_of_types(FUNCTION_STATEMENT_TOKENS):
            return self._parse_function_statement()
        elif self._is_one_of_types(VAR_STATEMENT_TOKENS):
            return self._parse_var_statement()
        return self._parse_nondeclaring_statement()

    def _parse_nondeclaring_statement(self):
        """
        Find next non-declaring statememt and return its AST
        (IF, WHILE, PRINT, BLOCK are non-declaring statements)
        """
        if self._is_one_of_types({TokenType.IF}):
            return self._parse_if_statement()
        if self._is_one_of_types({TokenType.WHILE}):
            return self._parse_while_statement()
        if self._is_one_of_types({TokenType.PRINT}):
            return self._parse_print_statement()
        if self._is_one_of_types(BLOCK_OPENING_TOKENS):
            return self._parse_block_statement()
        return self._parse_expression_statement()

    def _parse_var_statement(self) -> VarStatement:
        log.info(AppType.PARSER, 'Started parsing VarStatement')
        name = self._consume_or_raise(IDENTIFIER_TOKENS, 'Expect variable name')
        initializer = self._expression() if self._is_one_of_types(EQUALS_TOKENS) else None
        self._consume_or_raise(STATEMENT_END_TOKENS, 'Expect statement terminator after value')
        return VarStatement(name, initializer)

    def _parse_expression_statement(self) -> ExpressionStatement:
        log.info(AppType.PARSER, 'Started parsing ExpressionStatement')
        expression = self._expression()
        self._consume_or_raise(STATEMENT_END_TOKENS, 'Expect statement terminator after expression')
        return ExpressionStatement(expression)

    def _parse_print_statement(self) -> PrintStatement:
        log.info(AppType.PARSER, 'Started parsing PrintStatement')
        print_value = self._expression()
        self._consume_or_raise(STATEMENT_END_TOKENS, 'Expect statement terminator after value')
        return PrintStatement(print_value)

    def _parse_block_statement(self) -> BlockStatement:
        log.info(AppType.PARSER, 'Started parsing BlockStatement')
        block_start_token = self._peek()
        block_content = []
        while self._peek() and not self._peek().token_type in BLOCK_CLOSING_TOKENS:
            try:
                block_content.append(self._parse_statement())
            except ParseError as error:
                self.error_handler.add_error(error)
                self._synchronize()
        self._consume_or_raise(
            BLOCK_CLOSING_TOKENS,
            f'Expect block closing symbol for block started on line {block_start_token.source_file_line_number}',
        )
        return BlockStatement(block_content)

    def _parse_if_statement(self) -> IfStatement:
        log.info(AppType.PARSER, 'Started parsing IfStatement')
        self._consume_or_raise({TokenType.LEFT_PAREN}, "Expect ( after 'if'")
        condition = self._expression()
        self._consume_or_raise({TokenType.RIGHT_PAREN}, "Expect ) after 'if' condition")

        then_branch = self._parse_statement()
        else_branch = self._parse_statement() if self._is_one_of_types({TokenType.ELSE}) else None
        return IfStatement(condition, then_branch, else_branch)

    def _parse_while_statement(self) -> WhileStatement:
        log.info(AppType.PARSER, 'Started parsing WhileStatement')
        self._consume_or_raise({TokenType.LEFT_PAREN}, "Expect ( after 'while'")
        condition = self._expression()
        self._consume_or_raise({TokenType.RIGHT_PAREN}, "Expect ) after 'while' condition")

        loop_body = self._parse_statement()
        return WhileStatement(condition, loop_body)

    def _parse_function_statement(self) -> FunctionStatement:
        log.info(AppType.PARSER, 'Started parsing FunctionStatement')

        # name
        name = self._consume_or_raise(IDENTIFIER_TOKENS, "Expected a function name")

        # parameters
        parameters = []
        self._consume_or_raise(GROUP_OPENING_TOKENS, "Expected open paren after function name")
        if not self._is_same_type(TokenType.RIGHT_PAREN):
            parameters.append(self._consume_or_raise(IDENTIFIER_TOKENS, "Expected parameter name"))
            while self._is_one_of_types(DELIMITER_TOKENS):
                if len(parameters) > 254:
                    self.error_handler.report_error(ParseError(
                        self._peek(), "Max allowed function parameters is 255")
                    )
                parameters.append(self._consume_or_raise(
                    IDENTIFIER_TOKENS, "Expected a name at parameter " + str(len(parameters) + 1))
                )
        self._consume_or_raise(GROUP_CLOSING_TOKENS, "Expected close paren after function parameters")

        # body
        self._consume_or_raise(BLOCK_OPENING_TOKENS, "Expected opening curly brace before function body")
        body = self._parse_block_statement()

        return FunctionStatement(name, parameters, body)

    def _parse_return_statmeent(self) -> ReturnStatement:
        log.info(AppType.PARSER, 'Started parsing ReturnStatement')
        pass

    def _parse_class_statement(self) -> ClassStatement:
        log.info(AppType.PARSER, 'Started parsing ClassStatement')
        pass

    # PARSING EXPRESSIONS -----------------------------------------------------------------------------

    def _expression(self):
        return self._assignment()

    def _assignment(self):
        expression = self._logic_or()
        if not self._is_one_of_types(EQUALS_TOKENS):
            return expression

        if not isinstance(expression, Variable):
            raise ParseError(token=self._peek_prev(), message='Invalid assignment target.')

        name = expression.name
        value = self._assignment()
        return Assign(name, value)

    def _logic_or(self):
        left_side = self._logic_xor()
        while self._is_one_of_types({TokenType.OR}):
            operator = self._peek_prev()
            right_side = self._logic_xor()
            left_side = Binary(left_side, operator, right_side)
        return left_side

    def _logic_xor(self):
        left_side = self._logic_and()
        while self._is_one_of_types({TokenType.XOR}):
            operator = self._peek_prev()
            right_side = self._logic_and()
            left_side = Binary(left_side, operator, right_side)
        return left_side

    def _logic_and(self):
        left_side = self._equality()
        while self._is_one_of_types({TokenType.AND}):
            operator = self._peek_prev()
            right_side = self._equality()
            left_side = Binary(left_side, operator, right_side)
        return left_side

    def _equality(self):
        """
        Checks for equality between two operands
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
        left_side = self._exponent()
        while self._is_one_of_types(FACTOR_TOKENS):
            operator = self._peek_prev()
            right_side = self._exponent()
            left_side = Binary(left_side, operator, right_side)
        return left_side

    def _exponent(self):
        """
        Exponentiation
        """
        left_side = self._unary()
        while self._is_one_of_types({TokenType.EXPONENT}):
            operator = self._peek_prev()
            right_side = self._unary()
            left_side = Binary(left_side, operator, right_side)
        return left_side

    def _unary(self):
        """
        Acts on a single operand
        """
        if self._is_one_of_types(UNARY_TOKENS):
            operator = self._peek_prev()
            right_side = self._unary()
            return Unary(operator, right_side)
        return self._call()

    def _call(self):
        """
        A function call
        """
        expression = self._primary()

        while True:
            if self._is_one_of_types([TokenType.LEFT_PAREN]):
                expression = self._function_call(expression)
            else:
                break

        return expression

    def _primary(self):
        """
        A primary rule
        """
        if self._is_one_of_types(LITERAL_TOKENS):
            return Literal(self._peek_prev())

        if self._is_one_of_types(IDENTIFIER_TOKENS):
            return Variable(self._peek_prev())

        if self._is_one_of_types(GROUP_OPENING_TOKENS):
            expression = self._expression()
            self._consume_or_raise(GROUP_CLOSING_TOKENS, 'Expected closing paren')
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

    def _function_call(self, function):
        """
        Gathers function and all arguments into a Call expression
        """
        arguments = []
        if not self._is_same_type(TokenType.RIGHT_PAREN):
            arguments.append(self._expression())
            while self._is_one_of_types([TokenType.COMMA]):
                if len(arguments) > 255:
                    self.error_handler.report_error(ParseError(
                        self._peek(), 'Too many function arguments, max is 255'))
                arguments.append(self._expression())

        closing_paren = self._consume_or_raise(
            TokenType.RIGHT_PAREN,
            'Expected closing paren ")" at end of function call')

        return Call(function, closing_paren, arguments)

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
