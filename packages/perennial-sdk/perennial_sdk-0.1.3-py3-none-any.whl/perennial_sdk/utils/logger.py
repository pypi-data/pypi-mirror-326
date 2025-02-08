import logging

# Setup for the general application logger
logger = logging.getLogger(__name__)
app_handler = logging.FileHandler('sdk.log')
app_handler.setLevel(logging.INFO)
app_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
app_handler.setFormatter(app_formatter)
logger.addHandler(app_handler)
logger.setLevel(logging.INFO)
