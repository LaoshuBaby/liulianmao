import os
from os.path import abspath, dirname, isfile, join
from typing import Optional

from .log import logger
from .storage import PROJECT_FOLDER, get_user_folder


def get_env(var_name: str, default: str) -> str:
    """
    尝试从环境变量获取值，如果失败，尝试从用户目录下和同目录下的文件读取，最后使用默认值。
    """

    def get_from_env(var_name: str) -> Optional[str]:
        """尝试从环境变量获取值。"""
        return os.environ.get(var_name)

    def get_from_user_folder(var_name: str) -> Optional[str]:
        """尝试从用户目录的文件夹读取。"""
        var_file_path = join(get_user_folder(), PROJECT_FOLDER, var_name)
        if isfile(var_file_path):
            try:
                with open(var_file_path) as f:
                    return f.read().strip()
            except Exception as e:
                logger.error(f"Error reading {var_name} from user folder file: {e}")
        return None

    def get_from_current_dir(var_name: str) -> Optional[str]:
        """尝试从当前文件所在目录读取。"""
        var_file_path = join(dirname(abspath(__file__)), var_name)
        if isfile(var_file_path):
            try:
                with open(var_file_path) as f:
                    return f.read().strip()
            except Exception as e:
                logger.error(f"Error reading {var_name} from current directory file: {e}")
        return None


    # 定义尝试顺序
    attempts = [get_from_user_folder, get_from_current_dir, get_from_env]

    for attempt in attempts:
        result = attempt(var_name)
        if result is not None:
            logger.trace("[Authentication]\n" + f"{var_name} = {result}")
            return result

    # 如果所有尝试都失败了，记录错误并返回默认值
    logger.error(f"{var_name} not found in environment variables, user folder, or current directory file, using default.")
    return default


# 获取API URL和API KEY
API_URL = get_env("OPENAI_BASE_URL", "https://api.openai.com")
API_KEY = get_env(
    "OPENAI_API_KEY",
    "You may need to check your environment variables' configure.",
)
