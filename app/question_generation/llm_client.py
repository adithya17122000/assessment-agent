import os
from dotenv import load_dotenv
from openai import OpenAI
from groq import Groq
from app.utils.time_logger_utils import timeit

load_dotenv()

AI_API_URL = os.getenv("AI_API_URL")
AI_API_KEY = os.getenv("AI_API_KEY")
MODEL = os.getenv("MODEL")
# client = OpenAI(base_url=AI_API_URL, api_key=AI_API_KEY)
client = Groq(api_key=AI_API_KEY)

def call_llm(prompt: str) -> str:
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
        max_completion_tokens=2048,
        top_p=1,
        reasoning_effort="low",
        stream=False,
        stop=None
    )

    content = completion.choices[0].message.content
    if not content:
        raise RuntimeError("LLM returned empty content — check prompt, model, or API response.")

    return content