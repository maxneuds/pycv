import logging
import sys


def setup_logging(level=logging.INFO):
    """
    Configures the root logger with a specific format including
    filename and line number.
    """
    # Create a custom format
    # %(filename)s : The name of the file.
    # %(lineno)d   : The line number where the log call was made.
    log_format = (
        "[%(asctime)s] %(levelname)-8s "
        "[%(filename)s:%(lineno)d] - %(message)s"
    )

    # Configure the root logger
    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ],
        datefmt="%H:%M:%S"
    )
