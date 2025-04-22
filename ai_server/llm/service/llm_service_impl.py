from openai import OpenAI
import os

class LLMServiceImpl:

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_response_from_openai(self, question: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}],
        )
        return response.choices[0].message.content.strip()
