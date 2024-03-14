import os
from loguru import logger
from datetime import datetime


user_home_path = os.path.expanduser("~")
log_folder_path = os.path.join(user_home_path, ".openai_utils")
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
