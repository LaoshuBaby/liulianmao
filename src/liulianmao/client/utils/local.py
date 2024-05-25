import os
import sys
from typing import List

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, "..", ".."))


from module.log import logger


def local_file_reader(path_list: List[str]) -> str:
    import requests

    logger.trace(f"[local_file_reader().path]: {path}")

    file_content = []
    for path in path_list:
        try:
            with open(path, "r", encoding="utf-8") as f:
                file_content.append(f.read())

        except Exception as e:
            logger.error(e)
            logger.warning(
                f"Failed to load file {path} from your local."
                + f"无法访问您本地的文件{path}。"
            )
            file_content.append(str(e))

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
