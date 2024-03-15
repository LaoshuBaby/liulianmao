import os
from datetime import datetime

from loguru import logger

from storage import get_user_folder

log_folder_path = os.path.join(str(get_user_folder()), ".openai_utils", "logs")
if not os.path.exists(log_folder_path):
    os.makedirs(log_folder_path)


logger.add(
    os.path.join(
        log_folder_path, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    ),
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
    level="TRACE",
)

logger.success("启动！")
logger.trace(log_folder_path)
