import os
import sys

import requests

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, ".."))

from module.authentication import API_KEY, API_URL
from module.log import logger

conversation = []


def get_user_id() -> str:
    import platform
    import uuid

    def get_mac_address():
        try:
            mac_hex = hex(uuid.getnode()).upper()
            mac = ":".join(
                mac_hex[i : i + 2] for i in range(2, len(mac_hex), 2)
            )
            return mac
        except:
            return None

    return (
        f"{platform.node()} ({get_mac_address()})"
        + " | "
        + f"{platform.python_implementation()} ({platform.python_build()[0]})"
    )


def zhipu_completion_vision(
    msg: str,
    image: str,
    model: str = "glm-4",
    amount: int = 1,
    temperature: float = 0.8,
    top_p: float = 0.6,
    max_tokens: int = 1024,
    no_history: bool = False,
):
    def trim_payload_for_logging(payload):
        import copy

        trimmed_payload = copy.deepcopy(payload)
        for message in trimmed_payload["messages"]:
            for content in message["content"]:
                if content["type"] == "image_url":
                    image_url = content["image_url"]["url"]
                    if len(image_url) > 1024:
                        content["image_url"][
                            "url"
                        ] = f"TOO LONG - len={len(image_url)}"
        logger.trace(trimmed_payload)
        return trimmed_payload

    if no_history:
        append_conversation = []
    else:
        append_conversation = conversation

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    payload = {
        "model": "glm-4v",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": msg},
                    {"type": "image_url", "image_url": {"url": image}},
                ],
            }
        ],
        "user_id": get_user_id(),
    }
    logger.trace("[Headers]\n" + f"{headers}")
    logger.trace("[Payload]\n" + f"{trim_payload_for_logging(payload)}")

    flag_echo_input = False
    if flag_echo_input:
        logger.debug("[Question]\n" + f"{msg}")
    else:
        logger.trace("[Question]\n" + f"{msg}")

    response = requests.post(
        API_URL + "/paas/v4/chat/completions",
        headers=headers,
        json=payload,
    )

    if response.status_code == 200:
        logger.trace("[Debug] response.status_code == 200")
        logger.trace(
            f"force_record: {response.status_code} {response.content.decode('utf-8')}"
        )
        logger.trace("[Response]\n" + str(response.json()))
        return response.json()
    else:
        logger.error(
            f"Error: {response.status_code} {response.content.decode('utf-8')}"
        )
        return {}


def zhipu_completion(
    msg: str,
    model: str = "glm-4",
    amount: int = 1,
    no_history: bool = False,
):
    """
    Sends a completion request to the Zhipu API.

    Args:
        msg (str): The question to be sent to the Zhipu API.
        model (str): The model to use for the completion.
        amount (int): The number of completions to request.
        no_history (bool): Whether to ignore previous conversation history.

    Returns:
        dict: The response from the Zhipu API.

    向智谱 API发送一个完成请求。

    参数：
        msg (str): 发送到Zhipu API的问题。
        model (str): 用于完成的模型。
        amount (int): 请求的完成数量。
        no_history (bool): 是否忽略之前的对话历史。

    返回：
        dict: 来自智谱 API的响应。
    """
    if no_history:
        append_conversation = []
    else:
        append_conversation = conversation
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    payload = {
        "model": "glm-4",
        "messages": append_conversation + [{"role": "user", "content": msg}],
        "user_id": get_user_id(),
    }
    logger.trace("[Headers]\n" + f"{headers}")
    logger.trace("[Payload]\n" + f"{payload}")

    flag_echo_input = False
    if flag_echo_input:
        logger.debug("[Question]\n" + f"{msg}")
    else:
        logger.trace("[Question]\n" + f"{msg}")

    response = requests.post(
        API_URL + "/paas/v4/chat/completions", headers=headers, json=payload
    )

    if response.status_code == 200:
        logger.trace("[Debug] response.status_code == 200")
        logger.trace(
            f"force_record: {response.status_code} {response.content.decode('utf-8')}"
        )
        # judge content_type
        try:
            logger.trace("[Response]\n" + str(response.json()))
        except Exception as e:
            logger.trace(e)
            logger.critical("RESPONSE NOT JSON")
        # judge json schema
        try:
            if no_history == False:
                conversation.append({"role": "user", "content": msg})
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


def zhipu_batch(
    input_file_id="",
    endpoint="/v4/chat/completions",
    completion_window="24h",
    metadata={"description": "sentiment classification"},
):
    def zhipu_batch_create(prompt_system: str, prompt_question: str):
        payload = {
            "model": "glm-4",
            "messages": [
                {"role": "system", "content": prompt_system},
            ]
            + [{"role": "user", "content": prompt_question}],
        }
        logger.trace("[Headers]\n" + f"{headers}")
        logger.trace("[Payload]\n" + f"{payload}")
        response = requests.post(
            API_URL + "/paas/v4/batches", headers=headers, json=payload
        )
        return response

    def zhipu_batch_retrieve():
        pass

    def zhipu_batch_files_create():
        pass

    def zhipu_batch_files_content():
        pass

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    response = zhipu_batch_create()

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
