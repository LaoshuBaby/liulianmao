import os
from os.path import abspath, dirname, isfile, join
from typing import Optional

from .log import logger
from .storage import PROJECT_FOLDER, get_user_folder


def get_env(var_name: str, default: str) -> str:
    """
    尝试从环境变量获取值，如果失败，尝试从用户目录下和同目录下的文件读取，最后使用默认值。
    """

    def get_valid_value(value: str) -> Optional[str]:
        """判断字符串是否有效，如果有效则返回该字符串，否则返回None。"""
        value = value.strip()
        if value and not value.startswith("#"):
            return value
        return None

    def read_and_log_file(file_path: str) -> Optional[str]:
        """读取文件，并记录每一行，返回第一个有效值。"""
        if isfile(file_path):
            try:
                with open(file_path) as f:
                    values = f.read().split("\n")
                    logger.trace("[Authentication]\n" + str(values))
                    for value in values:
                        valid_value = get_valid_value(value)
                        if valid_value:
                            return valid_value
            except Exception as e:
                logger.error(
                    f"Error reading from file: {file_path}, Error: {e}"
                )
        return None

    def get_from_env(var_name: str) -> Optional[str]:
        """尝试从环境变量获取值。"""
        return os.environ.get(var_name)

    def get_from_user_folder(var_name: str) -> Optional[str]:
        """尝试从用户目录的文件夹读取。"""
        """复用read_and_log_file函数。"""
        value = read_and_log_file(
            join(get_user_folder(), PROJECT_FOLDER, var_name)
        )
        return value

    def get_from_current_dir(var_name: str) -> Optional[str]:
        """尝试从当前文件所在目录读取。"""
        """复用read_and_log_file函数。"""
        value = read_and_log_file(join(dirname(abspath(__file__)), var_name))
        return value

    # 定义尝试顺序
    attempts = [get_from_user_folder, get_from_current_dir, get_from_env]

    for attempt in attempts:
        result = attempt(var_name)
        if result is not None:
            logger.trace("[Authentication]\n" + f"{var_name} = {result}")
            return result

    # 如果所有尝试都失败了，记录错误并返回默认值
    logger.error(
        f"{var_name} not found in environment variables, user folder, or current directory file, using default."
    )
    return default


# 用使用者最熟悉的语言以保证绝对的警觉，看到就能马上反映出来这不可以
warning_string = {
    "zh-Hans": "危险操作！请在向Issue反馈问题提交日志的时候不要将这部分内容提交",
    "en": "CAUTION: Dangerous operation! Please do not submit this section when providing logs in your issue report.",
}


def get_warning_string(langcode: str = "zh-Hans") -> str:
    """
    default langcode is zh-Hans
    """
    return warning_string.get(langcode)


# 获取API URL和API KEY
logger.trace("★" * 5 + get_warning_string() + "★" * 5)
API_URL = get_env("OPENAI_BASE_URL", "https://api.openai.com")
API_KEY = get_env(
    "OPENAI_API_KEY",
    "You may need to check your environment variables' configure.",
)
logger.trace("★" * 5 + get_warning_string() + "★" * 5)
