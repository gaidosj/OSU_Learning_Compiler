from enum import Enum
from src.tokens import TokenType, TokenOsu


class RuntimeDataType(Enum):
    """
    Different types of data stored in the RuntimeValue object (used by the interpreter)
    """
    INT = 'int'
    FLOAT = 'float'
    STRING = 'string'
    NULL = 'NULL'
    BOOL = 'bool'
    OBJECT = 'object'


class Environment:
    """
    Bidning of variable names and their values (for a given scope)
    """
    def __init__(self):
        pass


class RuntimeValue:
    """
    Stores values (and associated data type) computed during interpretation of the program
    """
    def __init__(self, value=None, data_type=RuntimeDataType.NULL):
        self.value = value
        self.data_type = data_type

    def is_truthy(self):
        """
        This method determines if current RuntimeValue evaluates to TRUE or FALSE
        """
        if self.data_type == RuntimeDataType.NULL:
            return False
        if self.data_type == RuntimeDataType.BOOL:
            return self.value
        return True


class LiteralTokenHelper:
    @staticmethod
    def get_runtime_value_for_token(token: TokenOsu):
        if token.token_type == TokenType.INT:
            return RuntimeValue(int(token.lexeme), RuntimeDataType.INT)

        if token.token_type == TokenType.FLOAT:
            return RuntimeValue(float(token.lexeme), RuntimeDataType.FLOAT)

        if token.token_type == TokenType.STRING:
            return RuntimeValue(token.lexeme[1: -1], RuntimeDataType.STRING)

        if token.token_type == TokenType.BOOL:
            return RuntimeValue(token.lexeme == 'TRUE', RuntimeDataType.BOOL)

        if token.token_type == TokenType.NULL:
            return RuntimeValue(None, RuntimeDataType.NULL)
