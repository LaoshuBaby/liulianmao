import os
import sys
from typing import List, Optional, Tuple

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, "..", ".."))

from module.const import all_available_languages
from module.log import logger


def filter_files(file_list: List[str], ignore_rules: List[Tuple[str, bool]]) -> List[str]:
    """根据忽略规则过滤文件列表。

    Args:
        file_list (List[str]): 原始文件列表。
        ignore_rules (List[Tuple[str, bool]]): 忽略规则列表，每个元素为一个元组，包含匹配模式和是否递归应用的标志。

    Returns:
        List[str]: 过滤后的文件列表。
    """
    filtered_list = []
    for file_path in file_list:
        ignore = False
        for pattern, recursive in ignore_rules:
            if recursive:
                if pattern in file_path:
                    ignore = True
                    break
            else:
                if pattern in os.path.basename(file_path):
                    ignore = True
                    break
        if not ignore:
            filtered_list.append(file_path)
    return filtered_list


def local_file_reader(path_list: List[str], ignore_rules: Optional[List[Tuple[str, bool]]] = None) -> str:
    """读取并处理指定路径列表中的文件内容，返回拼接后的结果。

    Args:
        path_list (List[str]): 文件路径列表。
        ignore_rules (Optional[List[Tuple[str, bool]]]): 忽略规则列表。

    Returns:
        str: 处理后的文件内容。
    """
    if ignore_rules is None:
        ignore_rules = []

    logger.trace(f"[local_file_reader().path_list]: {path_list}")

    def read_single_file(file_path: str) -> Optional[str]:
        """读取单个文件内容。

        Args:
            file_path (str): 文件路径。

        Returns:
            Optional[str]: 文件内容或None（如果文件不存在）。
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            logger.error(e)
            logger.warning(
                f"Failed to load file {file_path} from your local."
                + f"无法访问您本地的文件{file_path}。"
            )
            return None

    file_content = []
    for path in path_list:
        if os.path.isfile(path):
            file_content.append(read_single_file(path))
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_content.append(read_single_file(file_path))

    file_content = filter_files(file_content, ignore_rules)

    return "\n".join(filter(None, file_content))


def combine_dir_to_string(directory: str, ignore_rules: Optional[List[Tuple[str, bool]]] = None) -> str:
    """将目录内容组合成字符串。

    Args:
        directory (str): 目录路径。
        ignore_rules (Optional[List[Tuple[str, bool]]]): 忽略规则列表。

    Returns:
        str: 目录内容的字符串表示。
    """
    if ignore_rules is None:
        ignore_rules = []

    def should_ignore(file_path: str) -> bool:
        """判断文件是否应该被忽略。

        Args:
            file_path (str): 文件路径。

        Returns:
            bool: 如果文件应该被忽略，则返回True，否则返回False。
        """
        for pattern, recursive in ignore_rules:
            if recursive:
                if pattern in file_path:
                    return True
            else:
                if pattern in os.path.basename(file_path):
                    return True
        return False

    content_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if not should_ignore(file_path):
                content_list.append(f"File: {file_path}\nContent:\n{read_single_file(file_path)}\n")

    return "\n".join(content_list)
