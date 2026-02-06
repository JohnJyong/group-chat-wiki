import json
import lark_oapi as lark
from lark_oapi.api.im.v1 import ListMessageRequest, ReplyMessageRequest, ReplyMessageRequestBody, GetChatRequest
from lark_oapi.api.contact.v3 import GetUserRequest
from config import config

class FeishuBot:
    def __init__(self):
        self.client = lark.Client.builder() \
            .app_id(config.APP_ID) \
            .app_secret(config.APP_SECRET) \
            .build()

    def get_user_name(self, user_id):
        """
        Fetch user name by open_id. 
        Note: In production, cache this result to avoid rate limits.
        """
        request = GetUserRequest.builder() \
            .user_id_type("open_id") \
            .user_id(user_id) \
            .build()
            
        resp = self.client.contact.v3.user.get(request)
        if not resp.success():
            print(f"Failed to get user: {resp.code}, {resp.msg}")
            return "Unknown User"
        
        return resp.data.user.name

    def get_chat_history(self, chat_id, limit=50):
        """
        Fetch recent chat history.
        """
        request = ListMessageRequest.builder() \
            .container_id_type("chat") \
            .container_id(chat_id) \
            .page_size(limit) \
            .build()
            
        resp = self.client.im.v1.message.list(request)
        if not resp.success():
            print(f"Failed to get history: {resp.code}, {resp.msg}")
            return []
            
        messages = []
        # Reverse to get chronological order (oldest to newest)
        if resp.data.items:
            for msg in reversed(resp.data.items):
                # Filter for text messages only for now
                if msg.msg_type == "text":
                    try:
                        content = json.loads(msg.body.content)
                        text = content.get("text", "")
                        # Resolving sender name here is expensive (N+1 problem).
                        # For MVP, we use sender_id if not cached. 
                        # In real app: Use batch get or cache.
                        messages.append(f"[{msg.create_time}] {msg.sender.id}: {text}")
                    except:
                        continue
        return messages

    def reply_text(self, message_id, content):
        """
        Reply to a message.
        """
        request = ReplyMessageRequest.builder() \
            .message_id(message_id) \
            .request_body(ReplyMessageRequestBody.builder()
                .content(json.dumps({"text": content}))
                .msg_type("text")
                .build()) \
            .build()
            
        resp = self.client.im.v1.message.reply(request)
        if not resp.success():
            print(f"Failed to reply: {resp.code}, {resp.msg}")
