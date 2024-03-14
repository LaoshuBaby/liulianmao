import json

from log import logger
from openai_utils import ask


def chat():
    try:
        with open("tab_question.txt", "r", encoding="utf-8") as file:
            msg = file.read()
    except FileNotFoundError:
        print("File not found. Creating a new file.")
        with open("tab_question.txt", "w", encoding="utf-8") as file:
            file.write("Hello World!")
        return

    response = ask(msg)
    # print(response)


chat()
