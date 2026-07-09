import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

AI_API_URL = os.getenv("AI_API_URL")
AI_API_KEY = os.getenv("AI_API_KEY")
MODEL = os.getenv("MODEL")

client = OpenAI(base_url=AI_API_URL, api_key=AI_API_KEY)

def call_llm(prompt: str) -> str:
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
        top_p=1,
        max_tokens=4096,
        stream=False,
    )

    content = completion.choices[0].message.content
    if not content:
        raise RuntimeError("LLM returned empty content — check prompt, model, or API response.")

    return content