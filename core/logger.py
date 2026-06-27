import logging
import os
import config

os.makedirs("logs/", exist_ok=True)

logger = logging.getLogger(config.ASSISTANT_NAME)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

file_handler = logging.FileHandler(config.LOG_FILE)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)