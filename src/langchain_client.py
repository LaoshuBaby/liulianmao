import os

from langchain_openai import ChatOpenAI

API_URL = "https://aihubmix.com/v1"
API_SECRET_KEY = os.environ.get(
    "OPENAI_TOKEN",
    "You may need to check your environment variables' confogure.",
)

os.environ["OPENAI_API_KEY"] = API_SECRET_KEY
os.environ["OPENAI_BASE_URL"] = API_URL

llm = ChatOpenAI(openai_api_key=API_SECRET_KEY, openai_api_base=API_URL)


res = llm.invoke("how can geo-yuheng help with testing?")
# res = llm.predict("hello")
print(res)
