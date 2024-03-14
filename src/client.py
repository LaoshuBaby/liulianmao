from openai_utils import show
from log import logger
import json


def chat():
    try:
        with open("question.txt", "r", encoding="utf-8") as file:
            msg = file.read()
    except FileNotFoundError:
        print("File not found. Creating a new file.")
        with open("question.txt", "w", encoding="utf-8") as file:
            file.write("Hello World!")
        return

    response = show(msg)
    # print(response)


chat()
