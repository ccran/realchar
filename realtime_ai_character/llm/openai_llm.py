import os
from typing import Optional

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import BaseMessage, HumanMessage

from realtime_ai_character.database.chroma import get_chroma
from realtime_ai_character.llm.base import AsyncCallbackAudioHandler, AsyncCallbackTextHandler, LLM
from realtime_ai_character.logger import get_logger
from realtime_ai_character.utils import Character, timed

logger = get_logger(__name__)


class OpenaiLlm(LLM):
    def __init__(self, model):
        if os.getenv("OPENAI_API_TYPE") == "azure":
            from langchain.chat_models import AzureChatOpenAI

            self.chat_open_ai = AzureChatOpenAI(
                deployment_name=os.getenv("OPENAI_API_MODEL_DEPLOYMENT_NAME", "gpt-35-turbo"),
                model=model,
                temperature=0.5,
                streaming=True,
            )
        else:
            from langchain.chat_models import ChatOpenAI
            # model: Qwen1.5-14B-Chat Qwen1.5-32B-Chat chatglm3-6b Qwen1.5-7B-Chat
            # openai_api_base: http://localhost:20000/v1
            # openai_api_key: none
            self.chat_open_ai = ChatOpenAI(model='Qwen1.5-14B-Chat', temperature=0.5,
                                           openai_api_base="http://localhost:20000/v1",
                                           openai_api_key="none",
                                           streaming=True)

            # model: gpt-4
            # openai_api_base: https://api.gpt.biz/v1/
            # openai_api_key: os.getenv("OPENAI_API_KEY", ""),
            # self.chat_open_ai = ChatOpenAI(model='gpt-4', temperature=0.5,
            #                                openai_api_base="https://api.gpt.biz/v1",
            #                                openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            #                                streaming=True)
        self.config = {"model": model, "temperature": 0.5, "streaming": True}
        self.db = get_chroma()

    def get_config(self):
        return self.config

    @timed
    async def achat(
            self,
            history: list[BaseMessage],
            user_input: str,
            user_id: str,
            character: Character,
            callback: AsyncCallbackTextHandler,
            audioCallback: Optional[AsyncCallbackAudioHandler] = None,
            metadata: Optional[dict] = None,
            *args,
            **kwargs,
    ) -> str:
        # 1. Generate context
        context = self._generate_context(user_input, character)
        # logger.info(f'context:{context}')

        # 2. Add user input to history
        history.append(
            HumanMessage(
                content=character.llm_user_prompt.format(context=context, query=user_input)
            )
        )
        # logger.info(f'history:{history}')

        # 3. Generate response
        callbacks = [callback, StreamingStdOutCallbackHandler()]
        if audioCallback is not None:
            callbacks.append(audioCallback)
        response = await self.chat_open_ai.agenerate(
            [history], callbacks=callbacks, metadata=metadata
        )
        logger.info(f"Response: {response}")
        return response.generations[0][0].text

    def _generate_context(self, query, character: Character) -> str:
        docs = self.db.similarity_search(query)
        docs = [d for d in docs if d.metadata["character_name"] == character.name]
        logger.info(f"Found {len(docs)} documents")

        context = "\n".join([d.page_content for d in docs])
        return context
