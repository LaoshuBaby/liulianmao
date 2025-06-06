import os
import sys

import requests

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, ".."))

from module.authentication import API_KEY, API_URL
from module.log import logger
from module.storage import PROJECT_FOLDER, get_user_folder, init


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
    model: str = "glm-4v-plus",
    amount: int = 1,
    temperature: float = 0.8,
    top_p: float = 0.6,
    max_tokens: int = 1024,
    no_history: bool = False,
    **kwargs,
):
    def trim_payload_for_logging(payload):
        import copy

        trimmed_payload = copy.deepcopy(payload)
        for message in trimmed_payload["messages"]:
            for content in message["content"]:
                if content["type"] == "image_url":
                    image_url = content["image_url"]["url"]
                    if len(image_url) > 1024 * 1024:
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
        "model": model,
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
        "model": model,
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


def openai_images_generations(
    prompt,
    model: str = "cogview-3-plus",
    size: str = "1024x1024",
    quality: str = "standard",
    amount: int = 1,
):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "quality": quality,
        "n": amount,
    }

    logger.trace("[Headers]\n" + f"{headers}")
    logger.trace("[Payload]\n" + f"{payload}")

    response = requests.post(
        API_URL + "/paas/v4/images/generations", headers=headers, json=payload
    )

    def checker_size(size: str) -> bool:
        if size in [
            "1024x1024",
            "768x1344",
            "864x1152",
            "1344x768",
            "1152x864",
            "1440x720",
            "720x1440",
        ]:
            return True
        else:
            return False

    def download_image(url, save_path):
        from urllib.parse import parse_qs, urlparse

        parsed_url = urlparse(url)
        file_name = parsed_url.path.split("/")[-1]

        # 检查并根据内容类型更改文件后缀
        file_params = parse_qs(parsed_url.query)
        logger.trace(f"[extension_check:file_params]: {file_params}")
        response = requests.head(url)
        logger.trace(f"[extension_check:response.headers]: {response.headers}")

        def get_content_type():
            if file_params.get("rsct", []) != []:
                return str(file_params["rsct"][0])
            elif "Content-Type" in response.headers:
                return str(response.headers["Content-Type"])
            else:
                return ""

        if get_content_type():
            content_type = get_content_type()
            file_name_ext = content_type.split("/")[-1]
            file_name_stem = os.path.splitext(file_name)[0]
            file_name = f"{file_name_stem}.{file_name_ext}"

            def generate_unique_file_name(
                save_path, file_name_stem, file_name_ext
            ):
                full_file_name = f"{file_name_stem}.{file_name_ext}"
                full_save_path = os.path.join(save_path, full_file_name)
                file_number = 0

                # 检查文件是否存在，如果存在则在文件名中增加编号
                if os.path.exists(full_save_path):
                    logger.trace(
                        f"[file_name:collision.number]: {full_save_path}"
                    )
                    logger.trace(
                        f"[file_name:collision.exist]: {full_save_path}"
                    )
                    while os.path.exists(full_save_path):
                        logger.trace(
                            f"[file_name:collision.number]: {full_save_path}"
                        )
                        logger.trace(
                            f"[file_name:collision.exist]: {full_save_path}"
                        )
                        file_number += 1
                        full_file_name = (
                            f"{file_name_stem}({file_number}).{file_name_ext}"
                        )
                        full_save_path = os.path.join(
                            save_path, full_file_name
                        )

                    return f"{file_name_stem}({file_number}).{file_name_ext}"
                else:
                    return f"{file_name_stem}.{file_name_ext}"

            file_name = generate_unique_file_name(
                save_path, file_name_stem, file_name_ext
            )
        else:
            logger.warning(
                "haven't get image content_type and use default filename"
            )
            file_name = file_name
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
