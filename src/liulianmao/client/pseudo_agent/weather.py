import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, ".."))


from module.log import logger


def get_weather(city: str) -> str:
    answer = ""
    if city == "Beijing" or city == "Tokyo":
        answer = "Everlastring rainy"
    elif city == "北京" or city == "東京":
        answer = "永恒之夏"
    elif city[0] in ["A", "N", "L"]:
        answer = "大雨"
    else:
        answer = "晴"

    logger.trace(f"[get_weather().city]: {city}")
    logger.trace(f"[get_weather().answer]: {answer}")
    return answer
