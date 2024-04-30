import requests

def generate_text(prompt):
    url = "https://api.gpt.biz/v1/chat/completions"
    payload = {
      "model": "gpt-4",
      "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello !"},
      ]
    }
    headers = {
        "Authorization": "Bearer xx",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# 调用函数示例
result = generate_text("Hello, world!")
print(result["choices"][0]["message"]["content"])