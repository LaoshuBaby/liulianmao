import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, "..", ".."))


from module.log import logger


def url_reader(url: str, flag_keep_original: bool = False) -> str:
    """
    flag_keep_original = False  # shouldn't reduce space in a code file or ask not to modify original text
    """
    import requests

    logger.trace(f"[url_reader().url]: {url}")

    flag_have_protocal = False
    for protocal in ["https", "http"]:
        if protocal in url:
            flag_have_protocal = True
    if flag_have_protocal == False:
        logger.warning("您提交给url_reader的url没有指明协议，已自动补全https的协议头")
        url = "https://" + url

    logger.trace(f"[url_reader().url.fixed]: {url}")

    try:
        response = requests.get(
            url=url,
            headers={
                "User-Agent": "Mozilla/5.0 (liulianmao_url_reader/0.0.1)",
                "Referer": "https://github.com/LaoshuBaby/liulianmao/",
            },
        )
        logger.trace(f"[response.text]:\n{response.text}")
        logger.trace(f"[len(response.text)]: {len(response.text)}")

        LONG_PAGE_THERSHOLD = 1024
        CONTINUE_SPACE_THERSHOLD = 2

        if (len(response.text) > LONG_PAGE_THERSHOLD) and (
            flag_keep_original == False
        ):
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
        else:
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
