import os
import sys

import requests

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, ".."))

# unused import，pycharm会提醒，按F2可循环定向，可以用pycharm的 CSo ctrl shift O 快捷键去掉，
# ruff format 也能去掉
# pycharm(jetbrains系)快捷键（装个插件可以提醒漏按的快捷键，好用）：
# （我记住jetbrains这一套，就不想用vim了，但是如果盲打熟练的话，vim快捷键击键更少更方便）
# https://gist.github.com/boholder/da5f208aa160000d781a40d883cce53a
# https://github.com/halirutan/IntelliJ-Key-Promoter-X
from module.authentication import API_KEY, API_URL
from module.log import logger

conversation = []

# 大写的全局变量最好放方法外，global位置，即使是在方法内用的。
# 或者不当作全局变量，当方法内变量。
DEFAULT_API_URL = "http://localhost:11434"
# 这个API也是不变的，抽成全局变量，未来：
# 若动态变更则变成方法内get配置项（每次方法执行都能变）
# 若全局（应用生命周期）变更则 全局变量=配置项（应用重启会变）
COMPLETION_API_URL = DEFAULT_API_URL + "/v1/chat/completions"


# hoster 参数 unused，这个pycharm和ruff也会提醒
def llama_completion(prompt_system: str,prompt_question: str, model: str="llama3", temperature: float = 0.5, hoster: str="ollama",no_history:bool=False):
    # 为关键函数写文档，いい！
    """
    Sends a completion request to the llama API. OpenAI compatitable version.

    Args:
        question (str): The question to be sent to the llama API.
        model (str): The model to use for the completion.
        amount (int): The number of completions to request.

    Returns:
        The response from the llama API.

    发送一个完成请求到llama API。OpenAI兼容API。

    参数：
        question (str): 发送到llama API的问题。
        model (str): 用于完成的模型。
        amount (int): 请求的完成数量。

    返回：
        来自llama API的响应。
    """
    if no_history:
        append_conversation = []
    else:
        append_conversation = conversation
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt_system},
        ]
        + append_conversation
        + [{"role": "user", "content": prompt_question}],
        "temperature": temperature,
    }
    logger.trace("[Headers]\n" + f"{headers}")
    logger.trace("[Payload]\n" + f"{payload}")

    response = requests.post(COMPLETION_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        logger.trace("[Debug] response.status_code == 200")
        # judge content_type
        try:
            logger.trace("[Response]\n" + str(response.json()))
        except Exception as e:
            # loguru可以把异常包装成打印堆栈的异常，然后这个新异常还要处理
            # https://loguru.readthedocs.io/en/stable/overview.html#fully-descriptive-exceptions
            # 有时候我省事用 @logger.catch() 处理包装的异常
            # https://loguru.readthedocs.io/en/stable/overview.html#exceptions-catching-within-threads-or-main
            logger.trace(e)
            logger.critical("RESPONSE NOT JSON")
        # judge json schema
        try:
            if no_history == False:
                conversation.append(
                    {"role": "user", "content": prompt_question}
                )
                conversation.append(
                    {
                        "role": "system",
                        "content": response.json()["choices"][0]["message"][
                            "content"
                        ],
                    }
                )
        except Exception as e:
            logger.trace(e)
            logger.critical("WRONG RESPONSE SCHEMA")
        logger.trace("[History]\n" + str(conversation))
        return response.json()
    else:
        logger.trace("[Debug] response.status_code != 200")
        logger.error(
            f"Error: {response.status_code} {response.content.decode('utf-8')}"
        )
        return {}


def llama_completion_native():
    pass
