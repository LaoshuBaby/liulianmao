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
    with open(config_file_path, "r", encoding="utf-8") as file:
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


def completion_llama(question: str, model: str, amount: int = 1):
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


def generate_image(prompt, num_images: int = 1):
    config = load_conf()
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        # "model": "dall-e-3",
        "prompt": prompt,
        "size": "1024x1024",
        "quality": "standard",
        "n": 1,
    }

    logger.trace("[Headers]\n" + f"{headers}")
    logger.trace("[Payload]\n" + f"{payload}")

    response = requests.post(
        API_URL + "/v1/images/generations", headers=headers, json=payload
    )

    def download_image(url, save_path):
        from datetime import datetime
        from urllib.parse import parse_qs, urlparse

        parsed_url = urlparse(url)
        file_name = parsed_url.path.split("/")[-1]
        file_params = parse_qs(parsed_url.query)

        # 检查并根据内容类型更改文件后缀
        response = requests.head(url)
        if "Content-Type" in response.headers:
            content_type = response.headers["Content-Type"]
            file_extension = content_type.split("/")[-1]
            file_name_no_ext = os.path.splitext(file_name)[0]
            file_name = f"{file_name_no_ext}.{file_extension}"

        logger.trace(f"[file_name]: {file_name}")

        # 下载文件
        response = requests.get(url)
        if response.status_code == 200:
            full_save_path = os.path.join(save_path, file_name)
            with open(full_save_path, "wb") as f:
                f.write(response.content)
            print(f"File downloaded as {full_save_path}")
        else:
            print("Failed to download the file.")

    if response.status_code == 200:
        content_type = response.headers.get("Content-Type", "")

        if "application/json" in content_type:
            try:
                url_list_json = response.json().get("data", [])
                for url_item in url_list_json:
                    url = url_item.get("url")
                    logger.trace(f"[img_url]: {url}")

                    if url:
                        filename = url.split("/")[-1]
                        save_path = os.path.join(
                            get_user_folder(), PROJECT_FOLDER, "images"
                        )
                        logger.trace(f"[save_path]: {save_path}")
                        download_image(url, save_path)
                    else:
                        logger.warning("找不到URL。")
            except ValueError as e:
                logger.error("解析JSON失败。")
                logger.error(str(e))
        elif "image/png" in content_type:
            img_file_path = os.path.join(
                get_user_folder(),
                PROJECT_FOLDER,
                "images",
                "downloaded_image.png",
            )
            with open(img_file_path, "wb") as f:
                f.write(response.content)
            logger.success("图片文件保存成功。")
        else:
            logger.warning("未知的内容类型。")
    else:
        logger.error(f"响应状态码错误：{response.status_code}")
        logger.error(response.content.decode("utf-8"))


def ask(msg: str, available_models: List[str], default_amount: int = 1):
    response = completion(msg, available_models, amount=default_amount)
    try:
        choices = response.get("choices", [])

        # 使用.get()方法更安全地访问字典键值，以避免KeyError异常
        response_usage_completion_tokens = response.get("usage", {}).get(
            "completion_tokens", -1
        )
        response_usage_prompt_tokens = response.get("usage", {}).get(
            "prompt_tokens", -1
        )
        response_usage_total_tokens = response.get("usage", {}).get(
            "total_tokens", -1
        )

        # 假设这里有一些处理response的代码

    except Exception as e:
        # 记录关键错误信息而不是直接退出程序，提供更好的错误上下文
        logger.exception(f"An error occurred: {e}", exc_info=True)
        # 可以在这里处理特定的清理工作，如果有必要的话
        # 最后，可能会根据程序的需要选择是否退出
        # sys.exit()

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
    init()
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
    init()
    available_models = models()
    
    with open(
        os.path.join(
            get_user_folder(), PROJECT_FOLDER, "terminal", "question.txt"
        ),
        "r",
        encoding="utf-8",
    ) as f:
        msg = f.read()
    speech(msg)


def draw():
    init()
    available_models = models()
    with open(
        os.path.join(
            get_user_folder(), PROJECT_FOLDER, "terminal", "question.txt"
        ),
        "r",
        encoding="utf-8",
    ) as f:
        msg = f.read()
    generate_image(msg)


def main():
    logger.critical("THIS PROGRAM NOT INTENT TO RUN SUBMODULE".upper())
    exit(0)


if __name__ == "__main__":
    main()
