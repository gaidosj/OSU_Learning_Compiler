from src.logger import Logger as log


class ErrorHandler:
    def __init__(self, app_name=''):
        self.app_name=app_name
        self.errors = []

    def has_errors(self):
        return len(self.errors) > 0

    def add_error(self, error):
        self.errors.append(error)

    def log_errors(self):
        for error in self.errors:
            msg = '{}: {}'.format(
                type(error).__name__,
                error.message,
            )
            if error.token:
                msg += ' (line {}, around {})'.format(
                    error.token.source_file_line_number,
                    error.token.lexeme,
                )
            log.error(msg)

class ScanError(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message


class ParseError(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message


class InterpretError(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message
