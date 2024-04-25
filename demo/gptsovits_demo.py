import requests
import pyaudio
import json
import numpy as np

# 流式处理
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(2), channels=1, rate=32000, output=True)

url = "http://192.168.252.70:9880/tts"

payload = json.dumps({
    "ref_audio_path": "data/jz/jz.mp3",
    "prompt_text": "欢迎上车，我是星穹列车的领航员，姬子，相信我们将会共度一段有趣的旅程",
    "prompt_lang": "zh",
    "text": "注解实现操作日志的自动记录。这一创新简化了操作日志的记录流程，提高了开发效率和日志的规范性。",
    "text_lang": "zh",
    "streaming_mode": True
})
headers = {
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload, stream=True)
for chunk in response.iter_content(chunk_size=1024):
    # 处理响应内容
    audio_data = np.frombuffer(chunk, dtype=np.float32)
    # 将音频数据写入 PyAudio 输出流中播放
    stream.write(audio_data.tobytes())

stream.stop_stream()
stream.close()
p.terminate()
