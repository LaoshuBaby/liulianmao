import json

from log import logger
from openai_utils import ask


def init():
    file_list = [
        ("tab_question.txt", "Hello World!"),
        ("tab_answer.txt", "Hello! How can I assist you today?"),
    ]

    for file_name, default_content in file_list:
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                file.read()
        except FileNotFoundError:
            print(f"{file_name} not found. Creating a new file.")
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(default_content)


def chat():
    with open("tab_question.txt", "r", encoding="utf-8") as file:
        msg = file.read()

    flag_continue = True
    response = ask(msg)

    if flag_continue == False:
        with open("tab_answer.txt", "w", encoding="utf-8") as file:
            file.write(response)
    else:
        flag_end = False
        while flag_end == False:
            append_question = input("请输入追问：")
            if append_question != "END" and append_question != "":
                response = ask(append_question)
            else:
                flag_end = True
                break


init()
chat()
