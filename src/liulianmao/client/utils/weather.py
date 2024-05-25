import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, "..", ".."))


from module.log import logger


def get_weather(city: str) -> str:
    answer = ""
    if city == "Gensokyo":
        answer = "Everlastring rainy"
    elif city == "幻想乡":
        answer = "永恒之夏"
    else:
        template = (
            "| 温度 {tempature} | 湿度 {humidity} | 风力等级 {wind} | 天气状况 {weather} |"
        )

        import random

        weather_list = [
            "晴",
            "多云",
            "阴",
            "小雨",
            "大雨",
            "暴雨",
            "大暴雨",
            "小雪",
            "中雪",
            "大雪",
            "暴雪",
            "沙尘暴",
            "雾",
            "霾",
            "雨夹雪",
            "雷阵雨",
            "雷暴",
            "冰雹",
            "冻雨",
        ]

        answer = (
            template.replace(
                "{tempature}", f"{round(random.uniform(-25, 45), 1):.1f}"
            )
            .replace("{humidity}", f"{random.randint(0, 100)}%")
            .replace(
                "{wind}", f"{round(random.uniform(0.0, 40.0), 1):.1f} m/s"
            )
            .replace("{weather}", weather_list[random.randint(0, 18)])
        )

    logger.trace(f"[get_weather().city]: {city}")
    logger.trace(f"[get_weather().answer]: {answer}")
    return answer
