import json
import os
import sys

from module.log import logger


def is_serverlsss():
    flag_serverless = False
    result = {
        "flag_zeabur": os.environ.get("ZEABUR", ""),
        "flag_aws": os.environ.get("AWS", ""),
        "flag_aliyun": os.environ.get("ALIYUN", ""),
    }
    logger.trace(f"[is_serverless.result]: \n{json.dumps(result,indent=2)}")
    for key, value in result.items():
        if value != "":
            flag_serverless = True
            break
    return flag_serverless


if __name__ == "__main__":
    print(is_serverlsss())
