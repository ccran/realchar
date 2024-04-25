import uvicorn

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()


def fake_video_streamer():
    for i in range(10):
        yield b"some fake video bytes"


@app.get("/")
async def main():
    return StreamingResponse(fake_video_streamer())


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
