from langchain_openai import ChatOpenAI

from authentication import API_KEY, API_URL

llm = ChatOpenAI(openai_api_key=API_KEY, openai_api_base=API_URL)


def main():
    res = llm.invoke("how can geo-yuheng help with testing?")
    # res = llm.predict("hello")
    print(res)
