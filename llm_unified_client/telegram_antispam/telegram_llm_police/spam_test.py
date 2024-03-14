from openai_utils import show
from openai_utils import logger
import json


def chat():
    msg = """你好！世界！"""
    response = show(msg)
    # print(response)


def spam_detect():
    # 读取模板文件
    with open("template.txt", "r", encoding="utf-8") as template_file:
        template = template_file.read()

    # 读取句子文件
    with open("sentence.json", "r", encoding="utf-8") as sentence_file:
        sentences_raw = sentence_file.read()
        sentences = json.loads(sentences_raw)["data"]

    # 逐行处理句子
    count_success = 0
    count_failed = 0
    failed_collection = []
    for idx, sentence_dict in enumerate(sentences, start=1):
        sentence = sentence_dict["message"]
        status = sentence_dict["type"]
        msg = template.format(sentence=sentence)
        logger.info(sentence)
        logger.info(status)
        result = show(msg)
        if (result == status) or (result == "SPAM" and status == "SB"):
            count_success += 1
        else:
            count_failed += 1
            failed_collection.append(
                ("expected: " + status, "result: " + result, sentence)
            )

    logger.critical(f"count_success={count_success}")
    logger.critical(f"count_failed={count_failed}")
    for item in failed_collection:
        logger.error(item)


spam_detect()
