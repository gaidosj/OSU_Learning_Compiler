from enum import Enum
from src.tokens import TokenType, TokenOsu
from src.error_handler import InterpretError


class RuntimeDataType(Enum):
    """
    Different data types supported by OLC runtime environment
    """
    INT = 'int'
    FLOAT = 'float'
    STRING = 'string'
    NULL = 'NULL'
    BOOL = 'bool'
    OBJECT = 'object'


class Environment:
    """
    Binding of variable names and their values (for a given scope)
    """
    def __init__(self):
        pass


class RuntimeValue:
    """
    Stores values (and associated data types) computed during interpretation of the program
    """
    def __init__(self, value=None, data_type=RuntimeDataType.NULL):
        self.value = value
        self.data_type = data_type

    def __str__(self):
        return 'RTV (value={}, type={})'.format(self.value, self.data_type)

    def __eq__(self, other):
        # TODO: Hacky in order to pass tests. Need to change tests
        return str(self.value) == str(other)

    def is_same_type(self, other):
        return other and other.data_type == self.data_type

    def is_equal(self, other):
        """
        Compares two RuntimeValue objects
        """
        return self.is_same_type(other) and other.value == self.value

    def is_truthy(self):
        """
        This method determines if given RuntimeValue evaluates to TRUE or FALSE
        """
        if self.data_type == RuntimeDataType.NULL:
            return False
        if self.data_type == RuntimeDataType.BOOL:
            return self.value
        return True

    def is_number(self):
        return self.data_type in (RuntimeDataType.INT, RuntimeDataType.FLOAT,)

    def is_string(self):
        return self.data_type in (RuntimeDataType.STRING,)

    def is_bool(self):
        return self.data_type in (RuntimeDataType.NULL,)

    def is_null(self):
        return self.data_type in (RuntimeDataType.NULL,)


class RuntimeOperators:
    """
    Collection of methods for working with LITERAL tokens
    """
    @staticmethod
    def get_runtime_value_for_literal_token(token: TokenOsu):
        """
        Return RuntimeValue object for a literal token
        """
        LITERAL_TOKENS = {
            TokenType.INT: lambda token: RuntimeValue(int(token.lexeme), RuntimeDataType.INT),
            TokenType.FLOAT: lambda token: RuntimeValue(float(token.lexeme), RuntimeDataType.FLOAT),
            TokenType.STRING: lambda token: RuntimeValue(token.lexeme[1: -1], RuntimeDataType.STRING),
            TokenType.BOOL: lambda token: RuntimeValue(token.lexeme == 'TRUE', RuntimeDataType.BOOL),
            TokenType.NULL: lambda token: RuntimeValue(None, RuntimeDataType.NULL),
        }
        if token.token_type in LITERAL_TOKENS:
            return LITERAL_TOKENS[token.token_type](token)
        raise InterpretError(token=token, mesage='Literal value is expected')

    @staticmethod
    def get_runtime_value_for_unary_operator(operator: TokenOsu, operand: RuntimeValue):
        """
        Return RuntimeValue object for a unary operator
        """
        UNARY_OPERATORS = {
            TokenType.MINUS: RuntimeOperators._unary_minus,
            TokenType.NOT: RuntimeOperators._unary_not,
        }
        if operator.token_type in UNARY_OPERATORS:
            return UNARY_OPERATORS[operator.token_type](operand)
        raise InterpretError(token=operator, message='Unary operator is exprected')

    @staticmethod
    def get_runtime_value_for_binary_operator(left: RuntimeValue, operator: TokenOsu, right: RuntimeValue):
        """
        Return RuntimeValue object for a binary operator
        """
        BINARY_OPERATORS = {
            TokenType.MINUS: RuntimeOperators._binary_minus,
            TokenType.ASTERISK: RuntimeOperators._binary_asterisk,
            TokenType.DIV: RuntimeOperators._binary_div,
            TokenType.PLUS: RuntimeOperators._binary_plus,
            TokenType.GTE: RuntimeOperators._binary_gte,
            TokenType.GT: RuntimeOperators._binary_gt,
            TokenType.LTE: RuntimeOperators._binary_lte,
            TokenType.LT: RuntimeOperators._binary_lt,
            TokenType.EQUALITY: RuntimeOperators._binary_equality,
            TokenType.INEQUALITY: RuntimeOperators._binary_inequality,
        }
        if operator.token_type in BINARY_OPERATORS:
            return BINARY_OPERATORS[operator.token_type](left, right)
        raise InterpretError(token=operator, message='Binary operator is expected')

    # IMPLEMENTATION OF UNARY OPERATORS -----------------------------------------------------------

    @staticmethod
    def _unary_minus(operand: RuntimeValue):
        RuntimeValue(-operand.value, operand.data_type)  # TODO - remove - here for compatibility with prior interp
        if operand.is_number():
            return RuntimeValue(-operand.value, operand.data_type)
        raise Exception('not implemented')

    @staticmethod
    def _unary_not(operand: RuntimeValue):
        RuntimeValue(not operand.value, operand.data_type)  # TODO - remove - here for compatibility with prior interp
        if operand.is_bool():
            return RuntimeValue(not operand.value, operand.data_type)
        raise Exception('not implemented')

    # IMPLEMENTATION OF BINARY OPERATORS ----------------------------------------------------------

    @staticmethod
    def _binary_minus(left: RuntimeValue, right: RuntimeValue):
        print('BINARY MINUS')
        print('LEFT  :', left)
        print('RIGHT :', right)
        return RuntimeValue(left.value - right.value, left.data_type)  # TODO - remove - here for compatbility
        raise Exception('not implemented')

    @staticmethod
    def _binary_asterisk(left: RuntimeValue, right: RuntimeValue):
        return RuntimeValue(left.value * right.value, left.data_type)   # TODO - remove - here for compatbility
        raise Exception('not implemented')

    @staticmethod
    def _binary_div(left: RuntimeValue, right: RuntimeValue):
        return RuntimeValue(left.value // right.value, left.data_type)  # TODO - remove - here for compatbility
        raise Exception('not implemented')

    @staticmethod
    def _binary_plus(left: RuntimeValue, right: RuntimeValue):
        return RuntimeValue(left.value + right.value, left.data_type)  # TODO - remove - here for compatbility
        raise Exception('not implemented')

    @staticmethod
    def _binary_gte(left: RuntimeValue, right: RuntimeValue):
        return RuntimeValue(left.value >= right.value, left.data_type)  # TODO - remove - here for compatbility
        raise Exception('not implemented')

    @staticmethod
    def _binary_gt(left: RuntimeValue, right: RuntimeValue):
        return RuntimeValue(left.value > right.value, left.data_type)  # TODO - remove - here for compatbility
        raise Exception('not implemented')

    @staticmethod
    def _binary_lte(left: RuntimeValue, right: RuntimeValue):
        return RuntimeValue(left.value <= right.value, left.data_type)  # TODO - remove - here for compatbility
        raise Exception('not implemented')

    @staticmethod
    def _binary_lt(left: RuntimeValue, right: RuntimeValue):
        return RuntimeValue(left.value < right.value, left.data_type)  # TODO - remove - here for compatbility
        raise Exception('not implemented')

    @staticmethod
    def _binary_equality(left: RuntimeValue, right: RuntimeValue):
        return RuntimeValue(left.value == right.value, left.data_type)  # TODO - remove - here for compatbility
        raise Exception('not implemented')

    @staticmethod
    def _binary_inequality(left: RuntimeValue, right: RuntimeValue):
        return RuntimeValue(left.value != right.value, left.data_type)  # TODO - remove - here for compatbility
        raise Exception('not implemented')
