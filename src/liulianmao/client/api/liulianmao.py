import os
import sys
from datetime import datetime
from typing import List, Optional

import requests

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, "..", ".."))


from module.authentication import API_KEY, API_URL
from module.log import logger


def meow() -> Optional[bool]:
    response = requests.get(
        API_URL + "/v1/models",
        headers={
            "X-LIULIANMAO-SERIES": "Client",
        },
    )

    if response.status_code == 200:
        logger.trace("[Debug] response.status_code == 200")
        # judge mime
        try:
            logger.trace("[Response]\n" + str(response.json()))
        except Exception as e:
            logger.trace(e)
            logger.critical("RESPONSE NOT JSON")
        if (len(response.json().items()) == 1) and (
            response.json().get("liulianmao", "") == "meow"
        ):
            return True
        else:
            return False
    else:
        logger.trace("[Debug] response.status_code != 200")
        logger.error(
            f"Error: {response.status_code} {response.content.decode('utf-8')}"
        )
