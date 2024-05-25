import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, "..", ".."))


from module.log import logger


def get_traffic(city: str) -> float:
    import random

    answer = random.random()

    logger.trace(f"[get_traffic().city]: {city}")
    logger.trace(f"[get_traffic().answer]: {answer}")
    return answer
