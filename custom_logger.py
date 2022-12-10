import yaml
import os
import logging

try:
    from .custom_formatter import ConsoleFormatter, FileFormatter
except ImportError:
    from custom_formatter import ConsoleFormatter, FileFormatter


def read_config(file_path: str):
    with open(file_path, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)


try:
    config_file_path = os.environ["CONFIG_FILE_PATH"]
    logger_settings = read_config(config_file_path)["logger"]
except KeyError:
    logger_settings = read_config("./custom_logger/default_config.yaml")["logger"]
except FileNotFoundError:
    logger_settings = read_config("./default_config.yaml")["logger"]


_logging_levels = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}


def get_logger(
    module_name: str, level: str = logger_settings["level"]
) -> logging.Logger:
    level = _logging_levels[level.lower()]

    logger = logging.getLogger(module_name)
    logger.setLevel(level)
    logger.propagate = False

    # * Formatter
    formatter = ConsoleFormatter()
    file_formatter = FileFormatter()

    if logger_settings.get("independent_file_error_logging"):
        error_file_handler = logging.FileHandler(logger_settings["file_error_logging"])

        # * Set formats to handlers and add them to the logger
        error_file_handler.setFormatter(file_formatter)
        error_file_handler.setLevel(logging.ERROR)
        logger.addHandler(error_file_handler)

    # * File and Console handlers
    if logger_settings.get("file_logging"):
        general_file_handler = logging.FileHandler(logger_settings["file_path"])
        general_file_handler.setFormatter(file_formatter)
        logger.addHandler(general_file_handler)
    if logger_settings.get("terminal_logging"):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger
