import os
import sys

import requests

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, ".."))

from module.authentication import API_KEY, API_URL
from module.log import logger


def llama_completion(question: str, model: str, amount: int = 1):
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
