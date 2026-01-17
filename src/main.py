import logging
from lib.logger import setup_logging
from lib.pycv import PyCV

if __name__ == "__main__":
    # 1. Setup Logging
    setup_logging(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    # 2. Generate CV as PDF
    cv = PyCV()
    cv.generate_pdf()
