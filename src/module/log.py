import os

from hellologger import get_logger

from .const import get_user_folder, PROJECT_FOLDER

log_folder_path = os.path.join(str(get_user_folder()), PROJECT_FOLDER)


if not os.path.exists(os.path.join(log_folder_path,"log")):
    os.makedirs(os.path.join(log_folder_path,"log"))


logger = get_logger(
    log_path=log_folder_path,
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