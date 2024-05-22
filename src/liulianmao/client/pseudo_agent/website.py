import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, ".."))


from module.log import logger


def url_reader(url: str) -> str:
    import requests

    logger.trace(f"[url_reader().url]: {url}")

    flag_have_protocal = False
    for protocal in ["https", "http"]:
        if protocal in url:
            flag_have_protocal = True
    if flag_have_protocal == False:
        logger.warning("您提交给url_reader的url没有指明协议，已自动补全https的协议头")
    url = "https://" + url

    try:
        response = requests.get(
            url=url, headers={"User-Agent": "liulianmao_url_reader/0.0.1"}
        )
        answer = response.text
    except Exception as e:
        logger.error(e)
        logger.warning(
            "Failed to get url or can't access the site on your network."
            + "无法打开url或无法从您的网络上访问"
            + "建议您检查您的防火墙或代理设置"
        )
        answer = str(e)

    logger.trace(f"[url_reader().answer]: {answer}")
    return answer
