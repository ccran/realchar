import json
from asyncio import Event

import requests
from starlette.websockets import WebSocket
import numpy as np
from realtime_ai_character.audio.text_to_speech.base import TextToSpeech
from realtime_ai_character.logger import get_logger
from realtime_ai_character.utils import Singleton

logger = get_logger(__name__)

"""
    调用GPTSoVITS生成音频
"""

VOICE_PROMPT_MAPPING = {
    "jz": "欢迎上车，我是星穹列车的领航员，姬子，相信我们将会共度一段有趣的旅程",
    "swk": "妖孽，哪里跑!",
}


class GPTSoVITS(Singleton, TextToSpeech):
    async def stream(self, text: str,
                     websocket: WebSocket,
                     tts_event: Event,
                     voice_id: str,
                     first_sentence: bool,
                     language: str,
                     *args, **kwargs):
        url = "http://192.168.252.70:9880/tts"
        payload = json.dumps({
            "ref_audio_path": f"data/{voice_id}/{voice_id}.mp3",
            "prompt_text": VOICE_PROMPT_MAPPING.get(voice_id),
            "prompt_lang": language[:2],
            "text": text,
            "text_lang": language[:2],
            "streaming_mode": True
        })
        logger.info(f"payload:{payload}")
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload, stream=True)
        msgs = []
        for chunk in response.iter_content(chunk_size=1024):
            # 处理响应内容
            audio_data = np.frombuffer(chunk, dtype=np.float32)
            # 将音频数据写入 PyAudio 输出流中播放
            msgs.extend(audio_data.tobytes())
        await websocket.send_bytes(bytes(msgs))

    def __init__(self):
        super().__init__()
        logger.info("Initializing [GPTSoVITS] voices...")
