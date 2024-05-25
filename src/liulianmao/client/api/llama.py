import os
import sys

import requests

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, ".."))

from module.authentication import API_KEY, API_URL
from module.log import logger

def llama_completion(question: str, model: str, amount: int = 1):
    """
    Sends a completion request to the llama API.

    Args:
        question (str): The question to be sent to the llama API.
        model (str): The model to use for the completion.
        amount (int): The number of completions to request.

    Returns:
        The response from the llama API.

    发送一个完成请求到llama API。

    参数：
        question (str): 发送到llama API的问题。
        model (str): 用于完成的模型。
        amount (int): 请求的完成数量。

    返回：
        来自llama API的响应。
    """
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": question,
        "temperature": temperature,
        "n": amount,
    }
    logger.trace("[Headers]\n" + f"{headers}")
    logger.trace("[Payload]\n" + f"{payload}")
    response = requests.post(
        API_URL + "/completions", headers=headers, json=payload
    )
    return response
