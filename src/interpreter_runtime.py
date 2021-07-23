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
        return self.value == other

    def is_same_type(self, other):
        return other and other.data_type == self.data_type

    def is_strictly_equal(self, other):
        """
        Compares two RuntimeValue objects (both values and types have to match)
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

    def is_int(self):
        return self.data_type in (RuntimeDataType.INT,)

    def is_float(self):
        return self.data_type in (RuntimeDataType.FLOAT,)

    def is_string(self):
        return self.data_type in (RuntimeDataType.STRING,)

    def is_bool(self):
        return self.data_type in (RuntimeDataType.NULL,)

    def is_null(self):
        return self.data_type in (RuntimeDataType.NULL,)


class RuntimeOperators:
    """
    Collection of methods implementing behavior of operators on RuntimeValue objects
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
        raise InterpretError(token=token, message='Literal value is expected')

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
            return UNARY_OPERATORS[operator.token_type](operator, operand)
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
            return BINARY_OPERATORS[operator.token_type](left, operator, right)
        raise InterpretError(token=operator, message='Binary operator is expected')

    # IMPLEMENTATION OF UNARY OPERATORS -----------------------------------------------------------

    @staticmethod
    def _unary_minus(operator: TokenOsu, operand: RuntimeValue):
        if operand.is_number():
            return RuntimeValue(-operand.value, operand.data_type)
        raise InterpretError(token=operator, mesage='Minus operator is only implemented for numbers')

    @staticmethod
    def _unary_not(operator: TokenOsu, operand: RuntimeValue):
        if operand.is_bool():
            return RuntimeValue(not operand.value, operand.data_type)
        raise InterpretError(token=operator, message='Logical NOT is only implemented for booleans')

    # IMPLEMENTATION OF BINARY OPERATORS ----------------------------------------------------------

    @staticmethod
    def _binary_minus(left: RuntimeValue, operator: TokenOsu, right: RuntimeValue):
        """
        NUM - NUM -> INT (if both nums are INT) | FLOAT
        INT - BOOL -> INT (BOOL is interpreted as 0 / 1 for TRUE / FALSE)
        """
        if left.is_int() and right.is_int():
            return RuntimeValue(left.value - right.value, RuntimeDataType.INT)
        if left.is_number() and right.is_number():
            return RuntimeValue(left.value - right.value, RuntimeDataType.FLOAT)
        if left.is_int() and right.is_bool():
            return RuntimeValue(left.value - right.value, RuntimeDataType.INT)
        raise InterpretError(token=operator, mesage='Not implemented for given datatypes')

    @staticmethod
    def _binary_asterisk(left: RuntimeValue, operator: TokenOsu, right: RuntimeValue):
        """
        AMY (except NULL) * BOOL -> ANY
        STRING * INT -> STRING (Python string multiplication)
        NUM * NUM -> INT (if both nums are INT) | FLOAT
        NUM * BOOL -> INT (BOOL is interpreted as 0 / 1 for TRUE / FALSE)
        """
        # anything (except NULL) * bool -> same | empty, depening on the BOOL
        if not left.is_null() and right.is_bool():
            return RuntimeValue(left.value * right.value, left.data_type)
        if left.is_string() and right.is_int():
            return RuntimeValue(left.value * right.value, RuntimeDataType.STRING)
        if left.is_int() and right.is_int():
            return RuntimeValue(left.value * right.value, RuntimeDataType.INT)
        if left.is_number() and right.is_number():
            return RuntimeValue(left.value * right.value, RuntimeDataType.FLOAT)
        raise InterpretError(token=operator, mesage='Not implemented for given datatypes')

    @staticmethod
    def _binary_div(left: RuntimeValue, operator: TokenOsu, right: RuntimeValue):
        """
        INT / INT -> INT (// division)
        NUM / NUM -> FLOAT (/ division)
        """
        if left.is_int() and right.is_int():
            try:
                return RuntimeValue(left.value // right.value, RuntimeDataType.INT)
            except Exception:
                raise InterpretError(token=operator, mesage='Invalid operands for the division')

        if left.is_number() and right.is_number():
            try:
                return RuntimeValue(left.value / right.value, RuntimeDataType.FLOAT)
            except Exception:
                raise InterpretError(token=operator, mesage='Invalid operands for the division')

        raise InterpretError(token=operator, mesage='Not implemented for given datatypes')

    @staticmethod
    def _binary_plus(left: RuntimeValue, operator: TokenOsu, right: RuntimeValue):
        """
        STRING + STIRNG -> STRING (string concatenation)
        NUM + NUM -> INT (if both nums are INT) | FLOAT
        INT + BOOL -> INT (BOOL is interpreted as 0 / 1 for TRUE / FALSE)
        """
        if left.is_string() and right.is_string():
            return RuntimeValue(left.value + right.value, RuntimeDataType.STRING)
        if left.is_int() and right.is_int():
            return RuntimeValue(left.value + right.value, RuntimeDataType.INT)
        if left.is_number() and right.is_number():
            return RuntimeValue(left.value + right.value, RuntimeDataType.FLOAT)
        if left.is_int() and right.is_bool():
            return RuntimeValue(left.value + right.value, RuntimeDataType.INT)
        raise InterpretError(token=operator, mesage='Not implemented for given datatypes')

    @staticmethod
    def _compare_helper(left: RuntimeValue, operator: TokenOsu, right: RuntimeValue, comparator):
        """
        Strings can only be compared with strings. Numbers and bools can be compared among themselves
        """
        if (left.is_string() and right.is_string()):
            return RuntimeValue(comparator(left.value, right.value), RuntimeDataType.BOOL)
        if (left.is_number() or left.is_bool()) and (right.is_number() or right.is_bool()):
            return RuntimeValue(comparator(left.value, right.value), RuntimeDataType.BOOL)
        raise InterpretError(token=operator, mesage='Not implemented for given datatypes')

    @staticmethod
    def _binary_gte(left: RuntimeValue, operator: TokenOsu, right: RuntimeValue):
        return RuntimeOperators._compare_helper(left, operator, right, lambda left, right: left >= right)

    @staticmethod
    def _binary_gt(left: RuntimeValue, operator: TokenOsu, right: RuntimeValue):
        return RuntimeOperators._compare_helper(left, operator, right, lambda left, right: left > right)

    @staticmethod
    def _binary_lte(left: RuntimeValue, operator: TokenOsu, right: RuntimeValue):
        return RuntimeOperators._compare_helper(left, operator, right, lambda left, right: left <= right)

    @staticmethod
    def _binary_lt(left: RuntimeValue, operator: TokenOsu, right: RuntimeValue):
        return RuntimeOperators._compare_helper(left, operator, right, lambda left, right: left < right)

    @staticmethod
    def _binary_equality(left: RuntimeValue, operator: TokenOsu, right: RuntimeValue):
        return RuntimeValue(left.is_strictly_equal(right), RuntimeDataType.BOOL)

    @staticmethod
    def _binary_inequality(left: RuntimeValue, operator: TokenOsu, right: RuntimeValue):
        return RuntimeValue(not left.is_strictly_equal(right), RuntimeDataType.BOOL)


class Environment:
    """
    Binding of variable names and their values (for a given scope)
    """

    def __init__(self):
        """
        Store bindings between variable name and its value
        """
        self.bindings = {}

    def define(self, name: str, value: RuntimeValue):
        # TODO: Should name be TokenOsu ???
        # TODO: Explore preventing redefinition of existing variables
        self.bindings[name] = value

    def get(self, name: TokenOsu):
        if name and (name.lexeme in self.bindings):
            return self.bindings[name.lexeme]
        raise InterpretError(token=name, message='Undefined variable {}.'.format(name.lexeme))

    def assign(self, name: TokenOsu, value: RuntimeValue):
        if name.lexeme in self.bindings:
            self.bindings[name.lexeme] = value
            return
        raise InterpretError(token=name, message='Undefined variable {}.'.format(name.lexeme))
