import os
import sys
from typing import List, Optional, Tuple

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, "..", ".."))

from module.const import all_available_languages
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

    def read_single_image(file_path):
        import easyocr

        # if file_path have none-ascii char

        import re

        if re.search(r"[^\x00-\x7F]", file_path):
            logger.warning(
                f'The path "{file_path}"contains non-ASCII characters.'
            )
        else:
            logger.trace("The pathfile_pathonly contains ASCII characters.")

        logger.trace(f"Begin scan {file_path}")

        greater_china_common = ["en", "ch_sim"]
        lang_code = greater_china_common
        logger.trace(f"[lang_code]: {lang_code}")
        reader = easyocr.Reader(lang_code, gpu=False)
        detail = 1
        model_series = "zhipu"
        if model_series == "zhipu":
            detail = 0
            logger.warning(
                f"根据反馈，您所使用的{model_series}模型对复杂文本识别返回内容的结构识别能力较为有限，不建议使用较为详细的描述"
            )
        result = reader.readtext(file_path, detail=detail)
        return str(result)

    def read_single_file(file_path: str) -> Optional[str]:
        """读取单个文件内容。

        Args:
            file_path (str): 文件路径。

        Returns:
            Optional[str]: 文件内容或None（如果文件不存在）。
        """
        extension_image = [".jpg", ".png", ".gif", ".bmp", ".jpeg"]
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                file_extension = os.path.splitext(file_path)[1].lower()
                if file_extension == ".pdf":
                    logger.info("[file_type]: PDF")
                    return read_single_file_pdf(file_path)
                elif file_extension in extension_image:
                    logger.info(f"[file_type]: IMG ({file_extension})")
                    return read_single_image(file_path)
                else:
                    return file.read()
        except Exception as e:
            logger.error(e)
            logger.warning(
                f"Failed to load file {file_path} from your local."
                + f"无法访问您本地的文件{file_path}。"
            )
            return None

    def process_files_in_path_list(path_list) -> List[Optional[str]]:
        """
        处理路径列表中的所有文件。

        Args:
            path_list (List[str]): 文件路径列表。

        Returns:
            str: 处理后的文件内容。
        """
        file_content = []

        def recursive_read_files(path) -> List[Optional[Tuple[str, str]]]:
            """
            如果是文件，就返回这个文件内容，并封进list中。当然也可能是[None]
            如果是目录，就递归逐个调用，返回的依然是一个list，里面的多个元素可能是Tuple[str,str](第一个路径，第二个正文)或None
            """
            # 初始化文件内容列表
            logger.trace(f"{path} call recursive_read_files")
            file_content = []

            # 检查当前路径是否是文件
            if os.path.isfile(path):
                file_content.append((path, read_single_file(path)))
            # 如果是目录，则继续遍历
            elif os.path.isdir(path):
                logger.trace(f"{path}是文件夹")
                for file_or_dir in os.listdir(path):
                    if flag_recursive:
                        logger.trace(f"{path}是文件夹且要求继续递归查找")
                        # 递归调用以处理子路径
                        sub_path = os.path.join(path, file_or_dir)
                        file_content.extend(recursive_read_files(sub_path))
                    else:
                        logger.trace(f"{path}是文件夹但里面更深的文件夹不管了")
                        if os.path.isfile(file_or_dir):
                            file_content.append((path, read_single_file(path)))

            return file_content

        for path in path_list:
            file_content.extend(recursive_read_files(path))
        return file_content

    file_content = process_files_in_path_list(path_list)

    logger.trace(file_content)

    if len(file_content) == 1:
        answer = file_content[0][1]
    else:
        answer = ""
        for i in range(len(file_content)):
            answer += (
                f"File ({i+1}/{len(file_content)}): {file_content[i][0]}\n"
            )
            answer += ">" * 20 + "\n"
            answer += str(file_content[i][1]) + "\n"

    logger.trace(f"[local_file_reader().answer]: {answer}")
    return answer


def combine_dir_to_string(
    dictionary,
    ignore_rules: List[Tuple[str, bool]] = [
        ("__pycache__", False),
        (".git", True),
    ],
) -> str:
    def should_ignore(dictionary, root, ignore_rules):
        """
        根据忽略规则判断目录是否应该被忽略。
        :param dictionary: 当前目录路径
        :param root: 根目录路径
        :param ignore_rules: 忽略规则列表，每个规则是一个二元组，包含目录名和是否只在根目录下忽略
        :return: 如果应该忽略，返回True；否则返回False。
        # 如果只在根目录下忽略，检查当前目录是否为根目录下的直接子目录
        # 如果在任意位置都忽略，检查当前目录名是否匹配
        """
        for ignore_dir, only_root in ignore_rules:
            if only_root:
                if (
                    os.path.basename(dictionary) == ignore_dir
                    and os.path.dirname(dictionary) == root
                ):
                    return True
            else:
                if os.path.basename(dictionary) == ignore_dir:
                    return True
        return False

    def print_tree(dictionary, prefix="", ignore_rules=None, root=""):
        if ignore_rules is None:
            ignore_rules = []
        if root == "":
            root = dictionary
        files = []
        if prefix == "":
            print(dictionary)
        else:
            print(prefix + os.path.basename(dictionary))
        prefix = prefix.replace("├──", "│  ").replace("└──", "   ")

        try:
            files = os.listdir(dictionary)
        except PermissionError as e:
            print(f"PermissionError: {e}")
            return
        except FileNotFoundError as e:
            print(f"FileNotFoundError: {e}")
            return

        files.sort()
        entries = [os.path.join(dictionary, f) for f in files]

        for i, entry in enumerate(entries):
            if os.path.isdir(entry) and should_ignore(
                entry, root, ignore_rules
            ):
                continue
            connector = "├──" if i < len(entries) - 1 else "└──"
            if os.path.isdir(entry):
                print_tree(
                    entry,
                    prefix=prefix + connector,
                    ignore_rules=ignore_rules,
                    root=root,
                )
            else:
                print(prefix + connector + os.path.basename(entry))

    if ignore_rules is None:
        ignore_rules = []
    if root == "":
        root = dictionary
    if extensions is None:
        extensions = [".py", ".rs", ".json"]
    all_files_content = ""
    for root, dirs, files in os.walk(dictionary):
        dirs[:] = [
            d
            for d in dirs
            if not should_ignore(os.path.join(root, d), root, ignore_rules)
        ]
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                all_files_content += f"File: {file_path}\n```\n"
                with open(file_path, "r", encoding="utf-8") as f:
                    all_files_content += f.read()
                all_files_content += "\n```\n\n"
    return all_files_content
