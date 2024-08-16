import os
import sys
from datetime import datetime
from typing import List, Optional

import requests

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, "..", ".."))


from module.authentication import API_KEY, API_URL
from module.log import logger
from module.storage import PROJECT_FOLDER, get_user_folder, init

conversation = []


def openai_models(model_series: str = "") -> List[str]:
    """
    Fetches a list of available models from the OpenAI API.

    Args:
        model_series: A string to filter models by series.

    Returns:
        A list of strings representing the available models.
    """
    logger.debug(f"[model_series]: {model_series}")
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
                    if model_series != "" and model_series in value.lower():
                        collected_ids.append(value)
                    elif model_series == "":
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
        try:
            extracted_ids = extract_ids(response.json()["data"])
            logger.debug("[Available Models]\n" + str(extracted_ids))
            return extracted_ids

        except Exception as e:
            logger.error(
                f"Error: {response.status_code} {response.content.decode('utf-8')}"
            )
            return {}
    else:
        logger.trace("[Debug] response.status_code != 200")
        logger.error(
            f"Error: {response.status_code} {response.content.decode('utf-8')}"
        )
        return {}


def openai_audio_speech(
    msg,
    model: str = "tts-1",
    voice: str = "alloy",
    response_format: str = "mp3",
    speed: float = 1.0,
):
    """
    Generates audio speech from text using the specified OpenAI model.

    Args:
        msg: The text message to convert to speech.
        model: The model to use for speech generation.
        voice: The voice to use for speech generation.
        response_format: The format of the generated audio file.
        speed: The speed of the speech.

    Returns:
        None. The generated audio file is saved locally.
    """

    def validate_voice(voice: str) -> str:
        voice_list = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
        if voice not in voice_list:
            logger.error("voice not supported")
            return voice_list[0]
        else:
            return voice

    def validate_format(response_format: str) -> str:
        format_list = ["mp3", "opus", "aac", "flac", "wav", "pcm"]
        if response_format not in format_list:
            logger.error("responce_format not supported")
            return format_list[0]
        else:
            return response_format

    def validate_speed(speed: float) -> None:
        min_speed = 0.25
        max_speed = 4.0

        if speed > max_speed or speed < min_speed:
            logger.error("speed not supported")
            return 1.0
        else:
            return speed

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "input": msg,
        "model": model,
        "voice": validate_voice(voice),
        "response_format": validate_format(response_format),
        "speed": validate_speed(speed),
    }

    response = requests.post(
        API_URL + "/v1/audio/speech", json=data, headers=headers
    )

    if response.status_code == 200:
        current_time = datetime.now().isoformat(timespec="milliseconds")
        safe_filename = current_time.replace(":", "_")
        speech_file_path = os.path.join(
            get_user_folder(),
            PROJECT_FOLDER,
            "audios",
            f"tts_{safe_filename.lower()}.{response_format.lower()}",
        )
        with open(speech_file_path, "wb") as f:
            f.write(response.content)
        logger.success(f"音频文件保存成功。{speech_file_path}")
    else:
        logger.error(
            "生成语音失败。状态码：",
            response.status_code,
            "\n",
            response.content.decode("utf-8"),
        )


def openai_chat_completion_vision(
    msg: str,
    image: str,
    model: str = "gpt-4o",
    amount: int = 1,
    temperature: float = 0.5,
    top_p: float = 1.0,
    max_tokens: int = 2048,
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
    if image[0:4] == "http":
        image_url = image
    else:
        image_url = f"data:image/jpeg;base64,{image}"
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": msg},
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url},
                    },
                ],
            }
        ],
    }
    logger.trace("[Headers]\n" + f"{headers}")
    logger.trace("[Payload]\n" + f"{trim_payload_for_logging(payload)}")

    flag_echo_input = False
    if flag_echo_input:
        logger.debug("[Question]\n" + f"{msg}")
    else:
        logger.trace("[Question]\n" + f"{msg}")

    response = requests.post(
        API_URL + "/v1/chat/completions",
        headers=headers,
        json=payload,
    )

    if response.status_code == 200:
        logger.trace("[Debug] response.status_code == 200")
        logger.trace(
            f"force_record: {response.status_code} {response.content.decode('utf-8')}"
        )
        # judge mime
        try:
            logger.trace("[Response]\n" + str(response.json()))
        except Exception as e:
            logger.trace(e)
            logger.critical("RESPONSE NOT JSON")
        # judge schema
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


def openai_chat_completion(
    prompt_question,
    prompt_system,
    model,
    temperature: float = 0.5,
    max_tokens: int = 2048,
    top_p: float = 1.0,
    frequency_penalty: float = 0.0,
    presence_penalty: float = 0.0,
    stop=None,
    amount: int = 1,
    use_plugin: bool = False,  # 新增参数来控制是否使用插件
    no_history: bool = False,
) -> Optional[dict]:
    """
    Generates a chat completion using the specified OpenAI model.

    Args:
        prompt_question: The user's question.
        prompt_system: System-level information or context.
        model: The model to use for generating the completion.
        temperature: Controls randomness in the generation.
        max_tokens: The maximum number of tokens to generate.
        top_p: Controls diversity via nucleus sampling.
        frequency_penalty: Decreases the likelihood of repeating tokens.
        presence_penalty: Increases the likelihood of introducing new tokens.
        stop: Sequence where the API will stop generating further tokens.
        amount: The number of completions to generate.
        use_plugin: Whether to use a plugin for additional functionality.
        no_history: Whether to ignore previous conversation history.

    Returns:
        A dictionary containing the generated completion(s).
    """

    def validate_temperature(temperature: float) -> float:
        min_temperature = 0.0
        max_temperature = 1.0
        if temperature > max_temperature or temperature < min_temperature:
            logger.error("temperature not supported")
            return 0.5
        else:
            return temperature

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    # 初始化payload
    if no_history:
        append_conversation = []
    else:
        append_conversation = conversation
    payload = {
        "messages": (
            [{"role": "system", "content": prompt_system}]
            + append_conversation
            + [{"role": "user", "content": prompt_question}]
        ),
        "model": model,
        "temperature": validate_temperature(temperature),
        "max_tokens": max_tokens,
        "top_p": top_p,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty,
        "stop": stop,
        "n": amount,
    }

    # 如果启用插件，添加到payload中
    if use_plugin:
        payload["tools"] = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            },
                            "unit": {
                                "type": "string",
                                "enum": ["celsius", "fahrenheit"],
                            },
                        },
                        "required": ["location"],
                    },
                },
            }
        ]
        payload["tool_choice"] = (
            "auto",
        )  # auto is default, but we'll be explicit

    logger.trace("[Headers]\n" + f"{headers}")
    logger.trace("[Payload]\n" + f"{payload}")

    flag_echo_input = False
    if flag_echo_input:
        logger.debug("[Question]\n" + f"{prompt_question}")
    else:
        logger.trace("[Question]\n" + f"{prompt_question}")

    response = requests.post(
        API_URL + "/v1/chat/completions", headers=headers, json=payload
    )

    if response.status_code == 200:
        logger.trace("[Debug] response.status_code == 200")
        logger.trace(
            f"force_record: {response.status_code} {response.content.decode('utf-8')}"
        )
        # judge mime
        try:
            logger.trace("[Response]\n" + str(response.json()))
        except Exception as e:
            logger.trace(e)
            logger.critical("RESPONSE NOT JSON")
        # judge schema
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
    model: str = "dall-e-3",
    size: str = "1024x1024",
    quality: str = "standard",
    amount: int = 1,
):
    """
    Generates images based on the given prompt using the specified OpenAI model.

    Args:
        prompt: The text prompt to generate images from.
        model: The model to use for image generation.
        size: The size of the generated images.
        quality: The quality of the generated images.
        amount: The number of images to generate.

    Returns:
        None. The generated images are saved locally.
    """
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
        API_URL + "/v1/images/generations", headers=headers, json=payload
    )

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
