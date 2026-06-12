import logging
import os

def setup_logging():
    """Sets up a dual logging handler pipeline saving to local log files."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_format = logging.Formatter(
        '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s'
    )

    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.DEBUG)

    # Prevent duplicating handlers if setup is called multiple times
    if not logger.handlers:
        # File Handler (Captures everything down to DEBUG)
        file_handler = logging.FileHandler(os.path.join(log_dir, "bot.log"))
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(log_format)

        # Console Handler (Clean output for terminal interface)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter('[*] %(message)s'))

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

logger = setup_logging()