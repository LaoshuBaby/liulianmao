import requests
import os
import sys


current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, ".."))

from module.authentication import API_KEY, API_URL
from module.log import logger


def openai_models(model_series: str = ""):
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
        extracted_ids = extract_ids(response.json()["data"])
        logger.debug("[Available Models]\n" + str(extracted_ids))
        return extracted_ids
    else:
        logger.trace("[Debug] response.status_code != 200")
        logger.error(
            f"Error: {response.status_code} {response.content.decode('utf-8')}"
        )
        return {}
