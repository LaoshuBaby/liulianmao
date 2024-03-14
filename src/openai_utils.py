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


def load_conf():
    with open("tab_conf.json", "r") as file:
        config = json.load(file)

    system_role = config["system_message"]["content"]
    temperature = float(config["settings"]["temperature"])
    return system_role, temperature


conversation_history = []


def requester(question, model_type="gpt-4-turbo-preview"):
    system_content, temperature = load_conf()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": select_model(model_type),
        "messages": conversation_history
        + [
            {"role": "system", "content": system_content},
            {"role": "user", "content": question},
        ],
        "temperature": temperature,
        "max_tokens": 2048,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
        "stop": None,
        # "plugins": [
        #     {
        #         "name": "plugin_name_here",
        #         "parameters": {"param1": "value1", "param2": "value2"},
        #     }
        # ],
    }

    logger.trace(f"Headers: {headers}")
    logger.trace(f"Payload: {payload}")
    logger.trace(f"User question: {question}")

    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        # response_dict = response.json()
        # logger.trace(
        #     f"OpenAI Response: {json.dumps(response_dict, ensure_ascii=False, indent=4)}"
        # )
        # return response_dict
        response_data = response.json()
        # 更新对话历史
        conversation_history.append({"role": "user", "content": question})
        conversation_history.append(
            {
                "role": "system",
                "content": response_data["choices"][0]["message"]["content"],
            }
        )
        logger.debug("conversation_history")
        logger.debug(conversation_history)
        logger.trace(conversation_history)
        return response_data
    else:
        logger.error(
            f"Error: {response.status_code} {response.content.decode('utf-8')}"
        )
        return {}


def ask(msg: str):
    response = requester(msg)
    logger.debug(response)
    content = response["choices"][0]["message"]["content"]
    logger.success(content)
    return content


def init():
    file_list = [
        ("tab_question.txt", "Hello World!"),
        ("tab_answer.txt", "Hello! How can I assist you today?"),
    ]

    for file_name, default_content in file_list:
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                file.read()
        except FileNotFoundError:
            print(f"{file_name} not found. Creating a new file.")
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(default_content)


def chat():
    with open("tab_question.txt", "r", encoding="utf-8") as file:
        msg = file.read()

    flag_continue = True
    response = ask(msg)

    if flag_continue == False:
        with open("tab_answer.txt", "w", encoding="utf-8") as file:
            file.write(response)
    else:
        flag_end = False
        while flag_end == False:
            append_question = input("请输入追问：")
            if append_question != "END" and append_question != "":
                logger.info("请输入追问：" + append_question)
                response = ask(append_question)
            else:
                flag_end = True
                break


init()
chat()
