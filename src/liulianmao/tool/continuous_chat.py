from typing import List
import time
from queue import Queue


available_models = ["AI1", "AI2"]
max_rounds = 10


model_queue = Queue()
for model in available_models:
    model_queue.put(model)


response_buffer = None


def ask(msg: str, current_model: str, **kwargs) -> str:
    print(f"Model {current_model} is processing the message: {msg}")
    return f"Response from {current_model}"


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
