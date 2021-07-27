from sys import stderr
from src.logger import Logger as log
from src.constants import AppType


class ErrorHandler:
    def __init__(self):
        self.errors = []

    def has_errors(self):
        return len(self.errors) > 0

    def report_error(self, error):
        self.errors.append(error)

    def log_errors(self):
        for error in self.errors:
            print('ERROR:', error.token, '\n\n')
            # if isinstance(error, ParseError):
            #     message = "Parse error on line {} for token {}: {}".format(
            #         error.token.source_file_line_number,
            #         error.token,
            #         error.message,
            #     )
            #     log.info(AppType.PARSER, message)
            # elif isinstance(error, InterpretError):
            #     message = "Runtime error on line {} for token {}: {}".format(
            #         error.token.source_file_line_number,
            #         error.token,
            #         error.message,
            #     )
            #     log.info(AppType.INTERPRETER, message)
            # else:
            #     log.info(AppType.INTERPRETER, f'generic exception {error}')


class ParseError(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message


class InterpretError(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message
