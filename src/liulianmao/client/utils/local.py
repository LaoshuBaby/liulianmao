import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, "..", ".."))


from module.log import logger


def local_file_reader(path: str) -> str:
    import requests

    logger.trace(f"[local_file_reader().path]: {path}")

    try:
        with open(path,"r",encoding="utf-8") as f:
            file_content=f.read()
        answer = file_content
    except Exception as e:
        logger.error(e)
        logger.warning(
            "Failed to load file from your local."
            + "无法访问您本地的文件。"
        )
        answer = str(e)

    logger.trace(f"[local_file_reader().answer]: {answer}")
    return answer
