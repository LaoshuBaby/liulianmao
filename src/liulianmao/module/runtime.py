import json
import os
import sys


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
