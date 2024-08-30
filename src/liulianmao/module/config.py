import json
import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, ".."))


from module.log import logger
from module.runtime import is_serverlsss
from module.storage import PROJECT_FOLDER, get_user_folder


def load_conf():
    config_file_path = os.path.join(
        get_user_folder(), PROJECT_FOLDER, "assets", "config.json"
    )
    if is_serverlsss() == True:
        logger.warning("LIULIANMAO RUNNING IN SERVERLESS ENVIRONMENT")
        logger.trace(
            "[Config]\n"
            + str({"environ": {"LIULIANMAO_RUNTIME": "SERVERLESS"}})
        )
        return {"environ": {"LIULIANMAO_RUNTIME": "SERVERLESS"}}
    else:
        with open(config_file_path, "r", encoding="utf-8") as file:
            config = json.load(file)
        logger.trace(
            "[Config]\n"
            + str({**config, **{"environ": {"LIULIANMAO_RUNTIME": "LOCAL"}}})
        )
        return {**config, **{"environ": {"LIULIANMAO_RUNTIME": "LOCAL"}}}
