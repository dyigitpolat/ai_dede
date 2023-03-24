from context_management.context_manager import ContextManager
from language_model_handling.openai_client import OpenAIClient
from input_processing.input_processing import InputProcessor
from output_processing.output_processing import OutputProcessor
from chat_history.chat_history import ChatHistory
from prompts.prompts import Prompts

class AIDede:
    def __init__(self):
        self.dede = OpenAIClient()
        self.context_manager = ContextManager([self.dede.chat_history])

    def respond(self, text):
        text = InputProcessor().process(text)

        response = self.dede.respond(text)
        self.context_manager.update()

        return OutputProcessor().process(response)
    
    def get_state_dict(self):
        state_dict = {}
        state_dict["message_history"] = self.dede.chat_history.messages
        state_dict["context_summary"] = self.context_manager.context_summary
        return state_dict

    def load_from_state_dict(self, state_dict):
        self.dede.chat_history.messages = state_dict["message_history"]
        self.context_manager.context_summary = state_dict["context_summary"]
        self.context_manager.chat_histories = [self.dede.chat_history]