import requests

url = 'http://127.0.0.1:8000'
response = requests.get(url, stream=True)
for chunk in response.iter_content(chunk_size=1024):
    # 处理响应内容
    print(chunk)
