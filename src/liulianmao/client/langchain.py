import os
import sys

from langchain_openai import ChatOpenAI

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_dir, ".."))

from module.authentication import API_KEY, API_URL
from module.log import logger

llm = ChatOpenAI(openai_api_key=API_KEY, openai_api_base=API_URL)


def chat():
    res = llm.invoke("how can geo-yuheng help with testing?")
    # res = llm.predict("hello")
    print(res)


def main():
    logger.critical("THIS PROGRAM NOT INTENT TO RUN SUBMODULE".upper())
    exit(0)


if __name__ == "__main__":
    main()
