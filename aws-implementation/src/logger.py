import logging
import os
import datetime

LOG_FILE =f"{datetime.now().strftime('%Y-%m-%d')}.log"
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
os.makedirs(os.path.dirname(logs_path), exist_ok=True)
logging.basicConfig(
    filename=logs_path,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)
def log_exception(error):
    logger.error(f"Exception occurred: {str(error)}", exc_info=True)    
