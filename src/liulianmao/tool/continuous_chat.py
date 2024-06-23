import json
import os
import sys
import time
from queue import Queue
from typing import List

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, ".."))

from client.api.openai import openai_models
from client.core import ask
from module.config import load_conf
from module.log import logger
from module.model import select_model
from module.storage import PROJECT_FOLDER, get_user_folder, init

models_room = ["zhipu", "llama"]
max_rounds = 10

config = load_conf()


model_queue = Queue()
for model in models_room:
    model_queue.put(model)


response_buffer = "你好！"

# def ask(
#     msg: str,
#     available_models: List[str] = [],
#     default_amount: int = 1,
#     model_series: str = "openai",
#     no_history: bool = False,
#     **kwargs,
# ):

#     return f"Response from {model}"


def get_available_models(model_series: str) -> List[str]:
    if model_series == "openai":
        available_models = openai_models("gpt")
    elif model_series == "zhipu":
        available_models = ["glm-4", "glm-3-turbo", "glm-4v"]
    elif model_series == "llama":
        available_models = ["llama3"]
    else:
        available_models = []


def communicate():
    global response_buffer
    round_counter = 0

    while not model_queue.empty() and round_counter < max_rounds:
        current_model = model_queue.get()

        available_models = get_available_models(current_model)

        ai_output = ask(
            msg=response_buffer,
            available_models=available_models,
            model_series=current_model,
        )[0]
        logger.success(
            f"Model {current_model} is processing the message: {ai_output}"
        )

        response_buffer = ai_output

        logger.info(
            f"Round {round_counter + 1}: {current_model} says:", ai_output
        )

        model_queue.put(current_model)

        round_counter += 1

        time.sleep(1)


communicate()
