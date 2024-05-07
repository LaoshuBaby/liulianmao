import os
import sys

import requests

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, ".."))

from module.authentication import API_KEY, API_URL
from module.log import logger

conversation = []


def zhipu_completion(
    prompt_question: str,
    prompt_system: str,
    model: str = "glm-4",
    amount: int = 1,
):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    payload = {
        "model": "glm-4",
        "messages": [
            {"role": "system", "content": prompt_system},
        ]
        + conversation
        + [{"role": "user", "content": prompt_question}],
    }
    logger.trace("[Headers]\n" + f"{headers}")
    logger.trace("[Payload]\n" + f"{payload}")
    response = requests.post(
        API_URL + "/paas/v4/chat/completions", headers=headers, json=payload
    )

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
            conversation.append({"role": "user", "content": prompt_question})
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
