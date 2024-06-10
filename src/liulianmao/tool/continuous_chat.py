import json
import os
import sys
import time
from queue import Queue
from typing import List

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, ".."))

from module.config import load_conf
from module.log import logger
from module.model import select_model
from module.storage import PROJECT_FOLDER, get_user_folder, init
from module.client.core import ask

models_room = ["AI1", "AI2"]
max_rounds = 10

config = load_conf()


model_queue = Queue()
for model in models_room:
    model_queue.put(model)


response_buffer = None


def completion(
    prompt_question: str,
    prompt_system: str = config["system_message"]["content"],
    model: str = "glm-4",
    amount: int = 1,
    no_history: bool = False,
):
    print(f"Model {model} is processing the message: {prompt_question}")
    return f"Response from {model}"


def communicate():
    global response_buffer
    round_counter = 0

    while not model_queue.empty() and round_counter < max_rounds:
        current_model = model_queue.get()

        ai_output = ask(response_buffer, current_model)

        response_buffer = ai_output

        print(f"Round {round_counter + 1}: {current_model} says:", ai_output)

        model_queue.put(current_model)

        round_counter += 1

        time.sleep(1)


communicate()
