from src.interpreter_runtime import Environment


class Function:
    def __init__(self, declaration):
        self.declaration = declaration

    def get_arity(self):
        return len(self.declaration.parameters)

    def call(self, interpreter, arguments):
        environment = Environment(interpreter.environment)
        for i in range(len(self.declaration.parameters)):
            environment.define(self.declaration.parameters[i].lexeme, arguments[i])

        interpreter.execute_block(self.declaration.body, environment)

    def __str__(self):
        return '<function ' + self.declaration.name.lexeme + '>'
