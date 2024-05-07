def get_weather(city: str) -> str:
    if city == "Beijing" or "Tokyo":
        return "Everlastring rainy"
    elif city == "北京" or "東京":
        return "永恒之夏"
    elif city[0] in ["A", "N", "L"]:
        return "大雨"
    else:
        return "晴"
