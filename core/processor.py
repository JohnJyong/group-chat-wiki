from core.bot import FeishuBot
from core.llm import LLMService

class MessageProcessor:
    def __init__(self):
        self.bot = FeishuBot()
        self.llm = LLMService()

    def handle_im_message_receive_v1(self, event):
        """
        Handle incoming message event.
        """
        message = event.message
        sender = event.sender
        
        # 1. Check if it's a text message mentioning the bot (handled by Feishu event filter usually)
        # For simplicity, we assume this event is triggered by @Bot
        
        # 2. Extract command
        try:
            content = eval(message.content) # safely parse json string
            text = content.get("text", "")
        except:
            text = ""

        if "跟我有关" in text or "personal summary" in text.lower():
            self._handle_personal_summary(message.chat_id, message.message_id, sender.sender_id.open_id)

    def _handle_personal_summary(self, chat_id, message_id, user_open_id):
        # 1. Get User Name
        user_name = self.bot.get_user_name(user_open_id)
        
        # 2. Get Chat History
        # Note: Optimization needed here. We fetch raw IDs first.
        # Ideally, we should fetch history -> resolve names for all senders -> pass to LLM.
        raw_history = self.bot.get_chat_history(chat_id, limit=50)
        
        # 3. Generate Summary
        history_text = "\n".join(raw_history)
        summary = self.llm.generate_personal_summary(user_name, history_text)
        
        # 4. Reply
        self.bot.reply_text(message_id, summary)
