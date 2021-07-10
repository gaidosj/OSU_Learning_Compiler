from sys import stderr


class ErrorHandler:
    def __init__(self):
        self.output = stderr

    def report_error(self, module, line_num, message):
        self.output.write(
            module
            + " error on line "
            + line_num
            + " : "
            + message
        )
