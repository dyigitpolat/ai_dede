from language_model_handling.openai_client import OpenAIClient
from context_management.chat_history_distillation import ChatHistoryDistillation
from chat_history.chat_history import ChatHistory
from prompts.prompts import Prompts

class ContextManager:
    def __init__(self, chat_histories):
        self.chat_histories = chat_histories
        self.context_summary = ""

    def __partial_distill(self, chat_history, limit, head_length):

        if len(chat_history) > limit:
            tail = ChatHistory(list(chat_history.messages[:-head_length]))
            head = ChatHistory(list(chat_history.messages[-head_length:]))
            distilled_tail = ChatHistoryDistillation().distill(tail)
            chat_history.messages = list(distilled_tail.messages + head.messages)

    def __summarize_context(self):
        summarization_prompt_f = Prompts.conversation_summary_prompt_f
        summarization_prompt_start = summarization_prompt_f.format("below")
        summarization_prompt_end = summarization_prompt_f.format("above")

        prompt = summarization_prompt_start
        for chat_history in self.chat_histories:
            chat_history_without_system_prompt = ChatHistory(list(chat_history.messages))
            prompt += "\n\n--\n\n"
            prompt += chat_history_without_system_prompt.to_text()
            prompt += "\n\n--\n\n"
        prompt += summarization_prompt_end

        assistant = OpenAIClient()
        self.context_summary = assistant.respond(prompt)

    def update(self):
        for chat_history in self.chat_histories:
            self.__partial_distill(chat_history, 6, 2)
        
        self.__summarize_context()
        

    