import json
import os

import requests

from module.authentication import API_KEY, API_URL
from module.log import logger
from module.model import select_model
from module.storage import init, get_user_folder, PROJECT_FOLDER


def load_conf():
    with open("assets/config.json", "r") as file:
        config = json.load(file)

    system_role = config["system_message"]["content"]
    temperature = float(config["settings"]["temperature"])
    return system_role, temperature


conversation = []


def tts(msg):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {"model": "tts-1", "input": msg, "voice": "alloy"}
    response = requests.post(
        API_URL + "/v1/audio/speech", json=data, headers=headers
    )

    if response.status_code == 200:
        speech_file_path = os.path.join(
            get_user_folder(), PROJECT_FOLDER, "audios", "speech.mp3"
        )
        with open(speech_file_path, "wb") as f:
            f.write(response.content)
        logger.success("音频文件保存成功。")
    else:
        logger.error(
            "生成语音失败。状态码：",
            response.status_code,
            "\n",
            response.content.decode("utf-8"),
        )


def requester(question, model_type="gpt-4-turbo-preview"):
    system_content, temperature = load_conf()

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": select_model(model_type),
        "messages": (
            [{"role": "system", "content": system_content}]
            + conversation
            + [{"role": "user", "content": question}]
        ),
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

    logger.trace("[Headers]\n" + f"{headers}")
    logger.trace("[Payload]\n" + f"{payload}")

    flag_echo_input = False
    if flag_echo_input:
        logger.debug("[Question]\n" + f"{question}")
    else:
        logger.trace("[Question]\n" + f"{question}")

    response = requests.post(
        API_URL + "/v1/chat/completions", headers=headers, json=payload
    )

    if response.status_code == 200:
        conversation.append({"role": "user", "content": question})
        conversation.append(
            {
                "role": "system",
                "content": response.json()["choices"][0]["message"]["content"],
            }
        )
        logger.trace("[History]\n" + str(conversation))
        logger.trace("[Response]\n" + str(response.json()))
        return response.json()
    else:
        logger.error(
            f"Error: {response.status_code} {response.content.decode('utf-8')}"
        )
        return {}


def ask(msg: str):
    response = requester(msg)
    content = response["choices"][0]["message"]["content"]
    logger.success("[Answer]\n" + content)
    return content


def chat():
    with open(
        os.path.join(
            get_user_folder(), PROJECT_FOLDER, "terminal", "question.txt"
        ),
        "r",
        encoding="utf-8",
    ) as file:
        msg = file.read()

    flag_continue = True
    response = ask(msg)

    if not flag_continue:
        with open(
            os.path.join(
                get_user_folder(), PROJECT_FOLDER, "terminal", "answer.txt"
            ),
            "w",
            encoding="utf-8",
        ) as file:
            file.write(response)
    else:
        flag_end = False
        while not flag_end:
            import time

            # 部分控制台输入是异步的，给足够的时间以保证不会打断输出
            time.sleep(0.05)
            logger.info("[Interaction] 请输入追问")
            append_question = input()
            append_question_judge = append_question.replace("\n", "").replace(
                " ", ""
            )
            if append_question_judge != "END" and append_question_judge != "":
                response = ask(append_question)
            else:
                flag_end = True
                break


def talk():
    with open("terminal/question.txt", "r", encoding="utf-8") as file:
        msg = file.read()
    tts(msg)


def main():
    init()
    chat()
    # talk()
