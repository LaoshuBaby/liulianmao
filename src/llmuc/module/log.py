import os

from hellologger import get_logger

from .const import PROJECT_FOLDER, get_user_folder

log_folder_path = os.path.join(str(get_user_folder()), PROJECT_FOLDER, "logs")


if not os.path.exists(log_folder_path):
    os.makedirs(log_folder_path)


logger = get_logger(
    log_path=log_folder_path,
    log_file="log_{time}.log",
    log_target={
        "local": True,
        "aliyun": False,
        "aws": False,
    },
    log_level={
        "local": "TRACE",
        "aliyun": "INFO",
    },
    **{},
)
logger.success("启动！")
logger.trace(log_folder_path)
