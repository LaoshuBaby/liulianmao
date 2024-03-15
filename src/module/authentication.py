import os
from os.path import isfile, join

from .log import logger
from .storage import get_user_folder, PROJECT_FOLDER


def get_env(var_name, default):
    """
    尝试从环境变量获取值，如果失败，尝试从用户目录的.openai_utils下和同目录下的文件读取，最后使用默认值。
    """
    # 从环境变量中获取
    value = os.environ.get(var_name)
    if value is not None:
        return value

    # 尝试从用户目录的.openai_utils文件夹读取
    var_file_path_user = join(get_user_folder(), PROJECT_FOLDER, var_name)
    if isfile(var_file_path_user):
        try:
            with open(var_file_path_user) as f:
                return f.read().strip()
        except Exception as e:
            logger.error(
                f"Error reading {var_name} from user folder file: {e}"
            )

    # 尝试从当前文件所在目录读取
    current_dir = os.path.dirname(os.path.abspath(__file__))
    var_file_path_current = join(current_dir, var_name)
    if isfile(var_file_path_current):
        try:
            with open(var_file_path_current) as f:
                return f.read().strip()
        except Exception as e:
            logger.error(
                f"Error reading {var_name} from current directory file: {e}"
            )

    # 记录错误并返回默认值
    logger.error(
        f"{var_name} not found in environment variables, user folder, or current directory file, using default."
    )
    return default


# 获取API URL和API KEY
API_URL = get_env("OPENAI_BASE_URL", "https://api.openai.com")
API_KEY = get_env(
    "OPENAI_API_KEY",
    "You may need to check your environment variables' configure.",
)
