from context_management.context_manager import ContextManager
from language_model_handling.agent import Agent
from input_processing.input_processing import InputProcessor
from output_processing.output_processing import OutputProcessor
from long_term_memory.conversation_memory import ConversationMemory
from chat_history.chat_history import ChatHistory
from prompts.prompts import Prompts

from llama_index import GPTSimpleVectorIndex

class AIDede:
    def __init__(self):
        self.dede = Agent(system_prompt="", pre_prompt=Prompts.dede_pre_prompt, post_prompt=Prompts.dede_post_prompt)
        self.context_manager = ContextManager([self.dede.chat_history])
        self.conversation_memory = ConversationMemory()

    def respond(self, text):
        text = InputProcessor().process(text)

        self.dede.system_prompt = self.context_manager.context_summary
        self.dede.system_prompt += f"\n\nConversation history: {self.conversation_memory.remember_for(self.context_manager.context_summary, text)}"
        response = self.dede.respond(text)

        self.context_manager.update()
        self.conversation_memory.add_conversation_pair(self.context_manager.context_summary, text, response)

        return OutputProcessor().process(response)
    
    def get_state_dict(self):
        state_dict = {}
        state_dict["message_history"] = self.dede.chat_history.messages
        state_dict["context_summary"] = self.context_manager.context_summary
        state_dict["conversation_memory"] = self.conversation_memory.conversation_index.save_to_string()
        return state_dict

    def load_from_state_dict(self, state_dict):
        self.dede.chat_history.messages = state_dict["message_history"]
        self.context_manager.context_summary = state_dict["context_summary"]
        self.context_manager.chat_histories = [self.dede.chat_history]
        self.conversation_memory.conversation_index = GPTSimpleVectorIndex.load_from_string(state_dict["conversation_memory"])