import asyncio

from langchain.chat_models import ChatOpenAI
import langchain
from langchain.schema import SystemMessage, HumanMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

print(f'langchain.__version__:{langchain.__version__}')


async def openai_chat():
    chat = ChatOpenAI(
        # Qwen1.5-14B-Chat Qwen1.5-32B-Chat
        model_name="Qwen1.5-7B-Chat",
        openai_api_base="http://192.168.252.70:20000/v1",
        openai_api_key="none",
        streaming=True,
    )

    # chat = ChatOpenAI(
    #     model_name="gpt-4",
    #     openai_api_base="https://api.gpt.biz/v1",
    #     openai_api_key="xx",
    #     streaming=True,
    # )

    messages = [
        SystemMessage(
            content="你是古人朱熹，你要用文言文的方式回答我"
        ),
        HumanMessage(
            content="你好，我的朋友，帮我写一首山水田园诗"
        ),
    ]
    response = await chat.agenerate(
        [messages], callbacks=[StreamingStdOutCallbackHandler()])
    print(f"Response: {response}")
    return response.generations[0][0].text


if __name__ == "__main__":
    asyncio.run(openai_chat())
