import os
import sys

import requests

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, ".."))

from module.authentication import API_KEY, API_URL
from module.log import logger

conversation = []


def llama_completion(
    prompt_system: str,
    prompt_question: str,
    model: str = "llama3",
    temperature: float = 0.5,
    hoster: str = "ollama",
    no_history: bool = False,
):
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

    DEFAULT_API_URL = "http://localhost:11434"
    API_URL = DEFAULT_API_URL
    response = requests.post(
        API_URL + "/v1/chat/completions", headers=headers, json=payload
    )

    if response.status_code == 200:
        logger.trace("[Debug] response.status_code == 200")
        # judge content_type
        try:
            logger.trace("[Response]\n" + str(response.json()))
        except Exception as e:
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
