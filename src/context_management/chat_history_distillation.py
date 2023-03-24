from chat_history.chat_history import ChatHistory
from language_model_handling.openai_client import OpenAIClient
from prompts.prompts import Prompts

class ChatHistoryDistillation:
    def __init__(self):
        pass
        
    def distill(self, chat_history):
        distillation_prompt = Prompts.conversation_distillation_prompt
        assistant = OpenAIClient()

        prompt_for_assistant = "\n\n--\n\n"
        prompt_for_assistant += chat_history.to_text()
        prompt_for_assistant += "\n\n--\n\n"
        prompt_for_assistant += distillation_prompt

        response = assistant.respond(prompt_for_assistant)

        distilled_chat_history = ChatHistory()
        for line in response.split("\n"):
            line = line.strip()
            if line != "":
                if len(line.split(":::")) == 2:
                    role, content = line.split(":::")
                    distilled_chat_history.append({"role": role, "content": content})

        return distilled_chat_history

        




        
