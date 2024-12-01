# utils/logger.py
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "name": record.name,
            "funcName": record.funcName,
            "lineno": record.lineno,
        }
        return json.dumps(log_entry)

def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)
    handler.setFormatter(JSONFormatter())
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

# Initialize logger
logger = setup_logger('agentic_ai_framework', 'framework.log')
