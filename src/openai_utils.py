import configparser
import json
import os

import requests

from log import logger
from model import select_model

api_url = "https://aihubmix.com/v1/chat/completions"
api_key = os.environ.get(
    "OPENAI_TOKEN",
    "You may need to check your environment variables' confogure.",
)


import json

def load_conf():
    with open("tab_conf.json", "r") as file:
        config = json.load(file)
    
    system_role = config["system_message"]["content"]
    temperature = float(config["settings"]["temperature"])
    return system_role, temperature


def requester(question, model_type="gpt-3.5-turbo"):
    system_content,  temperature = load_conf()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": select_model(model_type),
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": question},
        ],
        "temperature": temperature,
    }

    # 记录headers和payload
    logger.trace(f"Headers: {headers}")
    logger.trace(f"Payload: {payload}")

    # 记录用户的提问
    logger.trace(f"User question: {question}")

    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        response_dict = response.json()
        # 在得到响应后记录整个响应体，保留原样
        logger.trace(
            f"OpenAI Response: {json.dumps(response_dict, ensure_ascii=False, indent=4)}"
        )
        return response_dict
    else:
        logger.error(
            f"Error: {response.status_code} {response.content.decode('utf-8')}"
        )
        return {}


def ask(msg: str):
    response = requester(msg) 
    content = response["choices"][0]["message"]["content"]
    logger.success(content)
    return content
