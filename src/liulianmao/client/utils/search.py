import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, "..", ".."))

from module.log import logger


def get_search_result(keyword, engine="baidu") -> str:
    def get_search_url(keyword: str, engine: str):
        if engine.lower() == "baidu":
            search_url = f"https://www.baidu.com/s?wd={keyword}"
            # search_url = f"https://www.bing.com/search?q={keyword}"
        elif engine.lower() in ["google", "bing", "duckduckgo", "yandex"]:
            # search_url = f"https://www.bing.com/search?q={keyword}"
            # search_url = f"https://duckduckgo.com/?q={keyword}"
            # search_url = f"https://www.google.com/search?q={keyword}"
            # search_url = f"https://yandex.com/search/?text={keyword}"
            raise ValueError(f"搜索引擎 {engine} 可以解析但尚未实现。")
        else:
            raise ValueError(f"搜索引擎 {engine} 无法解析。")

        logger.trace(f"[get_search_result.keyword]: {keyword}")
        logger.trace(f"[get_search_result.engine]: {engine}")
        logger.trace(f"[get_search_result.search_url]: {search_url}")

        return search_url

    try:
        import requests

        response = requests.get(
            url=get_search_url(keyword, engine),
            headers={
                "User-Agent": "Mozilla/5.0 (liulianmao_get_search_result/0.0.1)",
                "Referer": "https://github.com/LaoshuBaby/liulianmao/",
            },
        )
        logger.trace(f"[response.text]:\n{response.text}")

        # 因为目前还没法从API直接获取，所以肯定要用bs清洗了

        CONTINUE_SPACE_THERSHOLD = 4

        import re

        def get_text_from_url(url_raw_text):
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(url_raw_text, "html.parser")
            return soup.get_text()

        souped_text = get_text_from_url(response.text)

        logger.trace(f"[souped_text]:\n{souped_text}")

        def reduce_spaces(input_string, continue_space_thershold):
            import re

            return re.sub(
                f" {continue_space_thershold+1,}",
                " " * continue_space_thershold,
                input_string,
            )

        pruned_text = "\n".join(
            list(
                filter(
                    bool,
                    [
                        (
                            reduce_spaces(i, CONTINUE_SPACE_THERSHOLD)
                            if (
                                i != ""
                                and bool(re.fullmatch(r"^[\s\n\t]*$", i))
                                == False
                            )
                            else ""
                        )
                        for i in souped_text.split("\n")
                    ],
                )
            )
        ).replace("\t", "")

        logger.trace(f"[pruned_text]:\n{pruned_text}")

        answer = pruned_text

    except Exception as e:
        logger.error(e)
        logger.warning(
            "Failed to search this keyword or can't access the engine on your network."
            + "无法搜索此关键词或搜索引擎无法从您的网络上访问"
            + "建议您检查您的防火墙或代理设置，以及检查该关键词在该搜索引擎是否为敏感词"
        )
        answer = str(e)

    return answer
