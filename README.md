# ai dede 

ai dede is an AI persona that uses ChatGPT to provide relevant and context-specific responses to users, with the added capability of long-term memory. This project integrates the llama-index library to enable the AI model to effectively incorporate historical information and respond in a more human-like manner.

## Installation

To get started with ai dede, make sure that you have the following dependencies installed:

- openai
- tenacity
- llama-index
- python-telegram-bot

Once you have installed these libraries, you will need to configure the API keys in `src/api_keys.py` and the authorized chats in `src/authorized_chats.py`. 

Here's an example of how you can configure the API keys:

```
# src/api_keys.py

openai_api_key = "openai_api_key"
telegram_bot_api_key = "telegram_bot_api_key"
```

## License

ai dede is distributed under the [MIT License](https://github.com/dyigitpolat/ai_dede/LICENSE).
