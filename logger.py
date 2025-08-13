# logger.py
# A simple logging configuration for the entire application.

import logging

def setup_logger():
    """
    Configures a basic logger that writes to a file named 'app.log'.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("weather-bot")

# Set up the logger when this module is imported.
logger = setup_logger()