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
def llama_completion(prompt_system: str, prompt_question: str, model: str = "llama3", temperature: float = 0.5, hoster: str = "ollama",
                     no_history: bool = False):
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
        # 既然这个方法里调用了response.json()，就正好把结果返回来，省得重复调用
        response_json = judge_response_content_type(response)

        # 好吧，是false的话用not好像比 is False 更好
        if not no_history:
            # 这一步无关响应的json格式是否异常，应该在try外，表明这个无关
            # （这样改也没改变执行顺序）
            conversation.append({"role": "user", "content": prompt_question})
            # 这部分没有return没有raise，说明它不影响执行顺序，
            # 抽成方法，减小读代码认知负担
            # （我不知道logger.critical会不会抛异常，不会吧）
            append_answer_to_history(response)

        logger.trace("[History]\n" + str(conversation))
        return response_json
    else:
        logger.trace("[Debug] response.status_code != 200")
        logger.error(
            f"Error: {response.status_code} {response.content.decode('utf-8')}"
        )
        return {}


def append_answer_to_history(response):
    try:
        # judge json schema
        answer = response.json()["choices"][0]["message"]["content"]
        conversation.append({"role": "system", "content": answer})
    except Exception as e:
        logger.trace(e)
        logger.critical("WRONG RESPONSE SCHEMA")


def judge_response_content_type(response):
    # judge content_type
    try:
        response_json = response.json()
        logger.trace("[Response]\n" + str(response_json))
        return response_json
    except Exception as e:
        # loguru可以把异常包装成打印堆栈的异常，然后这个新异常还要处理
        # https://loguru.readthedocs.io/en/stable/overview.html#fully-descriptive-exceptions
        # 有时候我省事用 @logger.catch() 处理包装的异常
        # https://loguru.readthedocs.io/en/stable/overview.html#exceptions-catching-within-threads-or-main
        logger.trace(e)
        logger.critical("RESPONSE NOT JSON")


def llama_completion_native():
    pass
