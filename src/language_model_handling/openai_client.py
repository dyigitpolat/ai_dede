from chat_history.chat_history import ChatHistory

import openai
import random

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)

class OpenAIClient:
    def __init__(self, model="gpt-3.5-turbo", system_prompt=""):
        self.chat_history = ChatHistory()
        self.model = model
        self.system_prompt = system_prompt

    def respond(self, text):
        print("Chat history length:", len(self.chat_history))
        print("Query:", text)
        self.chat_history.messages.insert(0, {"role": "system", "content": self.system_prompt})
        self.chat_history.append({"role": "user", "content": text})
        try:
            response = completion_with_backoff(
                model=self.model,
                messages=list(self.chat_history.messages),
                user=str(random.randint(0, 1000000000)),
            ).choices[0].message
            self.chat_history.append(response)
            self.chat_history.messages.pop(0)

            print("Response:", response.content)

            return response.content
        
        except Exception as e:
            print("Error: ", e)
            return "No response."