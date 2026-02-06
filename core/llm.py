from openai import OpenAI
from config import config

class LLMService:
    def __init__(self):
        self.client = OpenAI(
            api_key=config.OPENAI_API_KEY,
            base_url=config.OPENAI_BASE_URL
        )
        self.model = config.LLM_MODEL

    def generate_personal_summary(self, user_name, chat_history):
        """
        Generate a summary relevant to a specific user.
        """
        if not chat_history:
            return "暂无最近的聊天记录，无法生成摘要。"

        prompt = f"""
        你是一个专业的群聊助手。当前请求用户是：【{user_name}】。
        请阅读以下群聊记录（格式：[时间] 发送者: 内容），并提取**仅与该用户高度相关**的信息。
        
        聊天记录：
        {chat_history}
        
        请严格按以下格式输出 Markdown（无相关内容则跳过对应标题）：
        
        ### 🔴 待你处理 (Action Items)
        - [ ] 任务描述 (来源：发送者名)
        
        ### 🟡 提到你的 (Mentions)
        - 摘要内容
        
        ### 🟢 你的未决问题
        - 问题描述
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"LLM Error: {e}")
            return "抱歉，AI 总结服务暂时不可用。"
