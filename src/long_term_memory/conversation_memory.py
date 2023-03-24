from language_model_handling.openai_client import OpenAIClient
from prompts.prompts import Prompts

from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, Document
import llama_index

import time
import datetime

class ConversationMemory:
    def __init__(self, profile_id='default_profile'):
        self.profile_id = profile_id
        self.conversation_index = GPTSimpleVectorIndex([])

    def add_conversation_pair(self, context_summary, user_content, assistant_content):
        date = datetime.datetime.fromtimestamp(time.time()).strftime('%d/%m/%Y')
        clock = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M')
        text = Prompts.conversation_memo_prompt_f.format(
            date, clock, context_summary, user_content, assistant_content)

        self.conversation_index.insert(llama_index.Document(text))

    def remember_for(self, context_summary, query):
        text = Prompts.keyword_generation_prompt_f.format(context_summary, query)

        client = OpenAIClient(system_prompt=Prompts.keyword_generation_system_prompt)
        what_to_remember = client.respond(text)

        recall_result = None
        if len(what_to_remember):
            query_result = self.conversation_index.query("Inform about: " + what_to_remember)
            recall_result = f"\n\n{query_result.get_formatted_sources(2000)}"
            print("Recall result: ", recall_result)

        if recall_result is not None:
            return recall_result
        else:
            return "No previous information for this query."
