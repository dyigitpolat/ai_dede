from ai_dede.ai_dede import *

from telegram.ext import *
import telegram

import json

class TelegramBotUI:
    def __init__(self, token, authorized_chat_ids):
        self.application = Application.builder().token(token).build()
        self.authorized_chats = authorized_chat_ids

        
        self.state_dict = {}
        try:
            print("Loading state from state.json")
            with open("state.json", "r") as f:
                self.state_dict = json.load(f)

        except:
            print("Cannot find state creating state.json")
            with open("state.json", "w") as f:
                json.dump(self.state_dict, f)
        
        self.sessions = {}
        for chat_id in authorized_chat_ids:
            if f"{chat_id}" in self.state_dict:
                print(f"Restoring state for {chat_id}")
                ai_dede = AIDede()
                ai_dede.load_from_state_dict(self.state_dict[f"{chat_id}"])
                self.sessions[chat_id] = ai_dede
            else:
                self.sessions[chat_id] = AIDede()

    async def __message_handler(self, update, context):
        message = update.message
        chat_id = message.chat_id
        text = message.text

        await context.bot.send_chat_action(
            chat_id=chat_id, 
            action=telegram.constants.ChatAction.TYPING)

        try:
            if chat_id in self.authorized_chats:
                response = self.sessions[chat_id].respond(text)
                await context.bot.send_message(chat_id=chat_id, text=response)
            else:
                await context.bot.send_message(chat_id=chat_id, text=f"You are not authorized to use this bot. Chat id: {chat_id}")
        except Exception as e:
            print("Error: ", e)
            await context.bot.send_message(chat_id=chat_id, text="Something went wrong. Please try again later.")

        print("updating state file...")
        self.state_dict[f"{chat_id}"] = self.sessions[chat_id].get_state_dict()
        with open("state.json", "w") as f:
            json.dump(self.state_dict, f)
        print("updated state.")


    def start(self):
        self.application.add_handler(MessageHandler(filters.TEXT, self.__message_handler))
        self.application.run_polling(1.0)