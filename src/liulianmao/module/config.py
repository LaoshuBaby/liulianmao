import json
import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, ".."))


from module.log import logger
from module.storage import PROJECT_FOLDER, get_user_folder


def load_conf():
    def is_serverlsss():
        flag_serverless = False
        for key, value in {
            "flag_zeabur": os.environ.get("ZEABUR", ""),
            "flag_aws": os.environ.get("AWS", ""),
            "flag_aliyun": os.environ.get("ALIYUN", ""),
        }.items():
            if value != "":
                flag_serverless = True
                break
        return flag_serverless

    config_file_path = os.path.join(
        get_user_folder(), PROJECT_FOLDER, "assets", "config.json"
    )
    with open(config_file_path, "r", encoding="utf-8") as file:
        config = json.load(file)

    logger.trace("[Config]\n" + f"{config}")
    return config
