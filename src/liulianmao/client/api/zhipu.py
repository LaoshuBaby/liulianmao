import os
import sys

import requests

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, ".."))

from module.authentication import API_KEY, API_URL
from module.log import logger


def zhipu_completion(question: str, model: str = "glm-4", amount: int = 1):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {
        "model": "glm-4",
        "messages": [
	        {
	            "role": "user",
	            "content": question
	        }
	    ],
    }
    logger.trace("[Headers]\n" + f"{headers}")
    logger.trace("[Payload]\n" + f"{payload}")
    response = requests.post(
        API_URL + "/paas/v4/chat/completions", headers=headers, json=payload
    )
    return response
