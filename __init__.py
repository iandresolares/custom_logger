try:
    from .custom_logger import get_logger
except ImportError:
    from custom_logger import get_logger
