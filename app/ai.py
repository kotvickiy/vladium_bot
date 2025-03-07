from openai import OpenAI

from config import DS_TOKEN, GEMINI_TOKEN, DS_MODEL, GEMINI_MODEL


def ai(content ,token=DS_TOKEN, model=DS_MODEL):
    client = OpenAI(base_url='https://openrouter.ai/api/v1', api_key=token)
    completion = client.chat.completions.create(extra_body={}, model=model, messages=[{"role": "user", "content": content}])
    return completion.choices[0].message.content
