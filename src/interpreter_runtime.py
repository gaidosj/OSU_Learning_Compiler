from enum import Enum
from src.constants import Color, AppType
from src.logger import Logger as log
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
        return '({}){}'.format(self.data_type.name, self.value)

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


class Environment:
    """
    Binding of variable names and their values (for a given scope)
    """
    def __init__(self, enclosing_environment=None):
        """
        Store bindings between variable name and its value
        """
        self.enclosing_environment = enclosing_environment
        self.bindings = {}
        log.info(AppType.ENVIRONMENT, f'Created new environment: {str(self)}')

    def __del__(self):
        current = '[' + ';'.join([f'{name} = {value}' for name, value in self.bindings.items()]) + ']'
        out = f'{Color.BrightRed}{current}{Color.Reset}'
        if self.enclosing_environment:
            out += ' -> ' + str(self.enclosing_environment)
        log.info(AppType.ENVIRONMENT, f'Deleting current environment: {out}')

    def __str__(self):
        out = '[' + ';'.join([f'{name} = {value}' for name, value in self.bindings.items()]) + ']'
        if self.enclosing_environment:
            out += ' -> ' + str(self.enclosing_environment)
        return out

    def define(self, name: str, value: RuntimeValue):
        # TODO: Should name be TokenOsu ???
        # TODO: Explore preventing redefinition of existing variables
        self.bindings[name] = value
        log.info(AppType.ENVIRONMENT, f'Variable {name} defined. Updated environemnt: {str(self)}')

    def get(self, name: TokenOsu):
        if name and (name.lexeme in self.bindings):
            return self.bindings[name.lexeme]

        if self.enclosing_environment:
            return self.enclosing_environment.get(name)

        raise InterpretError(token=name, message='Undefined variable {}.'.format(name.lexeme))

    def assign(self, name: TokenOsu, value: RuntimeValue):
        if name.lexeme in self.bindings:
            self.bindings[name.lexeme] = value
            log.info(AppType.ENVIRONMENT, f'Variable {name.lexeme} assigned. Updated environemnt: {str(self)}')
            return

        elif self.enclosing_environment:
            self.enclosing_environment.assign(name, value)
            log.info(AppType.ENVIRONMENT, f'Variable {name.lexeme} assigned. Updated environemnt: {str(self)}')
            return

        raise InterpretError(token=name, message='Undefined variable {}.'.format(name.lexeme))
