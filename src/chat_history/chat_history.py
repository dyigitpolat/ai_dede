class ChatHistory:
    def __init__(self, messages = []):
        self.messages = list(messages)
    
    def to_text(self):
        text = ""
        for message in self.messages:
            text += f"{message['role']}::: {message['content']}"
            text += "\n\n"
        return text
    
    def append(self, message):
        self.messages.append(message)
    
    def __getitem__(self, index):
        return self.messages[index]
    
    def __len__(self):
        return len(self.messages)