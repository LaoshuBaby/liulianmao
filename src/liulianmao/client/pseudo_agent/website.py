import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, ".."))


from module.log import logger


def url_reader(url: str) -> str:
    import requests

    response = requests.get(
        url=url, headers={"User-Agent": "liulianmao_url_reader/0.0.1"}
    )
    answer = response.text

    logger.trace(f"[url_reader().url]: {url}")
    logger.trace(f"[url_reader().answer]: {answer}")
    return answer
