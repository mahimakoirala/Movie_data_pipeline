import logging
import os

os.makedirs("logs", exist_ok=True)  # Create the 'logs' directory if it doesn't exist

def get_logger(name):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s -%(levelname)s - %(name)s - %(filename)s:%(lineno)d - %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler("logs/pipeline.log", encoding = "utf-8"),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(name)
    return logger


        