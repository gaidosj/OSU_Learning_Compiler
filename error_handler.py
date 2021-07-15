from sys import stderr


class ErrorHandler:
    def __init__(self, output=stderr):
        self.output = output

    def report_error(self, error):
        if type(error) == type(ParseError):
            self.output.write(
                "Parse error on line "
                + error.token.source_file_line_number
                + " for token type "
                + error.token.type
                + " literal "
                + error.token.literal
                + " lexeme "
                + error.token.lexeme
                + ": "
                + error.message
            )


class ParseError(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message


class InterpretError(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message
