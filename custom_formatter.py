import logging


class ConsoleFormatter(logging.Formatter):

    debug_format = "%(asctime)s  [%(levelname)s] (%(module)s::%(funcName)s::%(lineno)d) %(message)s"
    normal_format = "%(asctime)s  [%(levelname)s] %(message)s"

    blue = "\x1b[36;21m"
    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self):
        super().__init__(fmt="%(levelno)d: %(msg)s", datefmt=None, style="%")

    def format(self, record):

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt

        # Replace the original format with one customized by logging level
        self.datefmt = "%d-%b-%y %H:%M:%S"
        if record.levelno == logging.DEBUG:
            self._style._fmt = ConsoleFormatter.debug_format
            format = ConsoleFormatter.debug_format
        else:
            self._style._fmt = ConsoleFormatter.normal_format
            format = ConsoleFormatter.normal_format

        self.FORMATS = {
            logging.DEBUG: ConsoleFormatter.grey + format + ConsoleFormatter.reset,
            logging.INFO: ConsoleFormatter.blue + format + ConsoleFormatter.reset,
            logging.WARNING: ConsoleFormatter.yellow + format + ConsoleFormatter.reset,
            logging.ERROR: ConsoleFormatter.red + format + ConsoleFormatter.reset,
            logging.CRITICAL: ConsoleFormatter.bold_red
            + format
            + ConsoleFormatter.reset,
        }

        log_fmt = self.FORMATS.get(record.levelno)

        # Restore the original format configured by the user
        self._style._fmt = format_orig

        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class FileFormatter(logging.Formatter):

    debug_format = "%(asctime)s  [%(levelname)s] (%(module)s::%(funcName)s::%(lineno)d) %(message)s"
    normal_format = "%(asctime)s  [%(levelname)s] %(message)s"

    def __init__(self):
        super().__init__(fmt="%(levelno)d: %(msg)s", datefmt=None, style="%")

    def format(self, record):

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt

        # Replace the original format with one customized by logging level
        self.datefmt = "%d-%b-%y %H:%M:%S"
        if record.levelno == logging.DEBUG:
            self._style._fmt = FileFormatter.debug_format
            format = FileFormatter.debug_format
        else:
            self._style._fmt = FileFormatter.normal_format
            format = FileFormatter.normal_format

        self.FORMATS = {
            logging.DEBUG: format,
            logging.INFO: format,
            logging.WARNING: format,
            logging.ERROR: format,
            logging.CRITICAL: format,
        }

        log_fmt = self.FORMATS.get(record.levelno)

        # Restore the original format configured by the user
        self._style._fmt = format_orig

        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
