import logging

def setupLogger():
    logging.basicConfig(
        filename='app.log',
        filemode='a',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        encoding='utf-8'
    )

def logInfo(message):
    logging.info(message)

def logError(message):
    logging.error(message)
