from src.constants import Color, AppType


class Logger:
    PARSER_LOGGER_ENABLED = True
    INTERPRETER_LOGGER_ENABLED = True
    ENVIRONEMNT_LOGGER_ENABLED = True

    @staticmethod
    def info(caller, message, color=None):
        if caller == AppType.PARSER and not Logger.PARSER_LOGGER_ENABLED:
            return
        if caller == AppType.INTERPRETER and not Logger.INTERPRETER_LOGGER_ENABLED:
            return
        if caller == AppType.ENVIRONMENT and not Logger.ENVIRONEMNT_LOGGER_ENABLED:
            return

        APP_SPECIFIC_COLOR = {
            AppType.PARSER: Color.BrightYellow,
            AppType.INTERPRETER: Color.BrightGreen,
            AppType.ENVIRONMENT: Color.BrightCyan,
        }
        color = color or APP_SPECIFIC_COLOR.get(caller, Color.BrightWhite)
        print(color, f'    {color}LOG: {caller.name} >>>>', message, Color.Reset)
