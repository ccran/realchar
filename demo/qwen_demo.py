from langchain.chat_models import ChatOpenAI
import langchain
from langchain.schema import SystemMessage, HumanMessage

print(langchain.__version__)
chat = ChatOpenAI(
    model_name="Qwen1.5-32B-Chat",
    openai_api_base="http://192.168.252.70:20000/v1",
    openai_api_key="none",
    streaming=False,
)
messages = [
    SystemMessage(
        content="你是古人朱熹，你要用文言文的方式回答我"
    ),
    HumanMessage(
        content="你好，我的朋友"
    ),
]
ans = chat(messages)
print(ans)
