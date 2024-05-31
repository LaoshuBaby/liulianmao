import os
import sys
from typing import List, Optional

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, "..", ".."))

from module.log import logger


def local_file_reader(path_list: List[str], flag_recursive=False) -> str:
    """读取并处理指定路径列表中的文件内容，返回拼接后的结果。

    Args:
        path_list (List[str]): 文件路径列表。
        flag_recursive (bool, optional): 是否递归处理文件夹。 Defaults to False.

    Returns:
        str: 处理后的文件内容。
    """

    logger.trace(f"[local_file_reader().path_list]: {path_list}")

    def read_single_file_pdf(file_path):
        """读取PDF文件并返回其内容作为纯文本字符串。

        Args:
            file_path (str): PDF文件路径。

        Returns:
            str: PDF文件内容作为纯文本字符串。
        """
        import pymupdf  # PyMuPDF

        text_content = []
        try:
            doc = pymupdf.open(file_path)
            for page in doc:
                text = page.get_text()
                text_content.append(text)
        except Exception as e:
            logger.error(f"Error while extracting text from PDF: {e}")
            return str(e)

        return "\n".join(text_content)

    def read_single_file(file_path: str) -> Optional[str]:
        """读取单个文件内容。

        Args:
            file_path (str): 文件路径。

        Returns:
            Optional[str]: 文件内容或None（如果文件不存在）。
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                if file_path.lower().endswith(".pdf"):
                    # 如果是PDF，调用read_single_file_pdf来处理
                    logger.info("[file_type]: PDF")
                    return read_single_file_pdf(file_path)
                elif file_path.lower().endswith(".jpg"):
                    logger.info("[file_type]: IMG")
                else:
                    return file.read()
        except Exception as e:
            logger.error(e)
            logger.warning(
                f"Failed to load file {file_path} from your local."
                + f"无法访问您本地的文件{file_path}。"
            )
            return None

    def process_files_in_path_list(path_list: List[str]) -> str:
        """
        处理路径列表中的所有文件。

        Args:
            path_list (List[str]): 文件路径列表。

        Returns:
            str: 处理后的文件内容。
        """
        file_content = []
        for path in path_list:
            if os.path.isfile(path):
                # path是文件
                file_content.append(read_single_file(path))
            else:
                # path是文件夹
                for file in os.listdir(path):
                    file_path = os.path.join(path, file)
                    if os.path.isfile(file_path):
                        file_content.append(read_single_file(file_path))

        return file_content

    file_content = process_files_in_path_list(path_list)

    logger.trace(file_content)

    if len(file_content) == 1:
        answer = file_content[0]
    else:
        answer = ""
        for i in range(len(file_content)):
            answer += f"File ({i+1}/{len(file_content)})\n"
            answer += ">" * 20 + "\n"
            answer += file_content[i] + "\n"

    logger.trace(f"[local_file_reader().answer]: {answer}")
    return answer
