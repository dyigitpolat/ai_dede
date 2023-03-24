from ui.telegram_bot_ui import *

import openai
import api_keys
import authorized_chats

if __name__ == "__main__":
    openai.organization = "org-YyEX4wI80xFZTZY6IjsS59V5"
    openai.api_key = api_keys.openai_api_key

    telegram_bot_ui = TelegramBotUI(
        api_keys.telegram_bot_api_key, 
        authorized_chats.authorized_chat_ids)

    telegram_bot_ui.start()
