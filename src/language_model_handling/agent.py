from language_model_handling.openai_client import OpenAIClient
from chat_history.chat_history import ChatHistory

class Agent:
    def __init__(self, system_prompt, pre_prompt, post_prompt):
        self.system_prompt = system_prompt
        self.pre_prompt = pre_prompt
        self.post_prompt = post_prompt
        self.chat_history = ChatHistory()
    
    def respond(self, user_input):
        client = OpenAIClient(system_prompt=self.system_prompt)
        client.chat_history.append({"role": "user", "content": self.pre_prompt})
        text = self.pre_prompt + user_input + self.post_prompt

        self.chat_history.append({"role": "user", "content": user_input})
        response = client.respond(text)
        self.chat_history.append({"role": "assistant", "content": response})
        return response