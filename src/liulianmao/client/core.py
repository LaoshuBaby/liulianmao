import json
import os
import sys
from typing import List

import requests

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, ".."))

from module.authentication import API_KEY, API_URL
from module.log import logger
from module.model import select_model
from module.storage import PROJECT_FOLDER, get_user_folder, init

conversation = []


def load_conf():
    config_file_path = os.path.join(
        get_user_folder(), PROJECT_FOLDER, "assets", "config.json"
    )
    with open(config_file_path, "r") as file:
        config = json.load(file)

    logger.trace("[Config]\n" + f"{config}")
    return config


def models():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    logger.trace("[Headers]\n" + f"{headers}")

    response = requests.get(API_URL + "/v1/models", headers=headers)

    def extract_ids(data):
        collected_ids = []

        for item in data:
            for key, value in item.items():
                if key == "id":
                    if value[0:3].lower() == "gpt":
                        collected_ids.append(value)

        return collected_ids

    if response.status_code == 200:
        logger.trace("[Debug] response.status_code == 200")
        # judge mime
        try:
            logger.trace("[Response]\n" + str(response.json()))
        except Exception as e:
            logger.trace(e)
            logger.critical("RESPONSE NOT JSON")
        extracted_ids = extract_ids(response.json()["data"])
        logger.debug("[Available Models]\n" + str(extracted_ids))
        return extracted_ids
    else:
        logger.trace("[Debug] response.status_code != 200")
        logger.error(
            f"Error: {response.status_code} {response.content.decode('utf-8')}"
        )
        return {}


def speech(msg):
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


def completion(question, available_models: List[str] = [], amount: int = 1):
    config = load_conf()
    model_type = config["model_type"]
    system_content = config["system_message"]["content"]
    temperature = float(config["settings"]["temperature"])

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": select_model(model_type, available_models, direct_debug=True),
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
        "n": amount,
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
        logger.trace("[Debug] response.status_code == 200")
        # judge mime
        try:
            logger.trace("[Response]\n" + str(response.json()))
        except Exception as e:
            logger.trace(e)
            logger.critical("RESPONSE NOT JSON")
        # judge schema
        try:
            conversation.append({"role": "user", "content": question})
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


def ask1(msg: str, available_models: List[str]):
    default_amount = 1
    response = completion(msg, available_models, amount=default_amount)
    try:
        response__choices__0__message__content = response["choices"][0][
            "message"
        ]["content"]
        response__usage__completion_tokens = response["usage"][
            "completion_tokens"
        ]
        response__usage__prompt_tokens = response["usage"]["prompt_tokens"]
        response__usage__total_tokens = response["usage"]["total_tokens"]
    except Exception as e:
        try:
            logger.critical(e)
            sys.exit()
        except Exception as ee:
            print(e, ee)
            sys.exit()
    logger.debug(
        "[Token Usage]\n"
        + json.dumps(
            {
                "response.usage.completion_tokens": response__usage__completion_tokens,
                "response.usage.prompt_tokens": response__usage__prompt_tokens,
                "response.usage.total_tokens": response__usage__total_tokens,
                "verify": f"{response__usage__completion_tokens} + {response__usage__prompt_tokens} = {response__usage__completion_tokens+response__usage__prompt_tokens}",
            },
            indent=2,
            ensure_ascii=False,
            sort_keys=False,
        )
    )
    logger.success("[Answer]\n" + response__choices__0__message__content)
    return response__choices__0__message__content


def ask(msg: str, available_models: List[str], default_amount: int = 1):
    response = completion(msg, available_models, amount=default_amount)
    try:
        choices = response["choices"]
        # 使用展平路径的变量命名方式
        response_usage_completion_tokens = response["usage"][
            "completion_tokens"
        ]
        response_usage_prompt_tokens = response["usage"]["prompt_tokens"]
        response_usage_total_tokens = response["usage"]["total_tokens"]
    except Exception as e:
        try:
            logger.critical(e)
            sys.exit()
        except Exception as ee:
            print(e, ee)
            sys.exit()

    # 使用展平路径的变量名进行日志记录
    logger.debug(
        "[Token Usage]\n"
        + json.dumps(
            {
                "response_usage_completion_tokens": response_usage_completion_tokens,
                "response_usage_prompt_tokens": response_usage_prompt_tokens,
                "response_usage_total_tokens": response_usage_total_tokens,
                # 计算验证
                "verify": f"{response_usage_completion_tokens} + {response_usage_prompt_tokens} = {response_usage_completion_tokens + response_usage_prompt_tokens}",
            },
            indent=2,
            ensure_ascii=False,
            sort_keys=False,
        )
    )

    # 根据choices的数量来输出
    for i, choice in enumerate(choices):
        logger.success(
            f"[Answer] ({i + 1}/{len(choices)})\n{choice['message']['content']}"
        )

    # 为了保持函数的兼容性（返回单一或多个答案），返回整个choices列表的消息内容
    return [choice["message"]["content"] for choice in choices]


def chat():
    available_models = models()

    with open(
        os.path.join(
            get_user_folder(), PROJECT_FOLDER, "terminal", "question.txt"
        ),
        "r",
        encoding="utf-8",
    ) as file:
        msg = file.read()

    flag_continue = True
    conversation = ask(msg, available_models)

    if not flag_continue:
        with open(
            os.path.join(
                get_user_folder(), PROJECT_FOLDER, "terminal", "answer.txt"
            ),
            "w",
            encoding="utf-8",
        ) as file:
            file.write(conversation)
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
                conversation = ask(append_question, available_models)
            else:
                flag_end = True
                break


def talk():
    with open("terminal/question.txt", "r", encoding="utf-8") as file:
        msg = file.read()
    speech(msg)


def main():
    logger.critical("THIS PROGRAM NOT INTENT TO RUN SUBMODULE".upper())
    exit(0)


if __name__ == "__main__":
    main()
