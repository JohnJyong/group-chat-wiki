# GroupChat Wiki (飞书群聊知识库 & 个人助理)

一个基于 AI (LLM) 和 Feishu Open API 的智能群聊助手。它不仅能将群聊碎片信息转化为结构化的 Wiki 知识库，还能为群成员提供个性化的 "跟我有关" 日报。

## 核心功能

1.  **GroupChat Wiki (群知识库):** 定时抓取群聊记录，自动提取决策、待办、链接，生成 Markdown 格式的日报并同步至飞书文档/多维表格。
2.  **Personal Assistant (个人助理):** 响应 `@Bot 跟我有关` 指令，智能过滤群消息，生成仅与该用户相关的待办和提及摘要。

## 技术栈

*   **Runtime:** Python 3.10+
*   **Web Framework:** Flask (用于接收飞书事件回调)
*   **SDK:** `lark-oapi` (飞书官方 SDK)
*   **AI:** OpenAI SDK (兼容 DeepSeek/Moonshot 等 OpenAI 格式接口)
*   **Test:** `pytest` (单元测试)

## 快速开始

### 1. 环境准备

```bash
# 克隆仓库
git clone https://github.com/JohnJyong/group-chat-wiki.git
cd group-chat-wiki

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 (环境变量)

复制 `.env.example` 为 `.env` 并填入你的配置：

```bash
cp .env.example .env
```

```ini
# Feishu / Lark App Config
APP_ID=cli_a1b2c3d4e5
APP_SECRET=your_app_secret
VERIFICATION_TOKEN=your_event_verification_token
ENCRYPT_KEY=your_event_encrypt_key

# OpenAI / LLM Config
OPENAI_API_KEY=sk-your-api-key
OPENAI_BASE_URL=https://api.deepseek.com  # 示例: DeepSeek
LLM_MODEL=deepseek-chat
```

### 3. 运行服务

```bash
python app.py
```
服务默认运行在 `http://0.0.0.0:3000`。

### 4. 飞书后台配置

1.  进入 [飞书开发者后台](https://open.feishu.cn/app)。
2.  **事件订阅:** 配置请求地址为 `http://your-server-ip:3000/webhook/event`。
3.  **权限管理:** 开通以下权限：
    *   `im:message:read_as_bot` (获取消息)
    *   `im:message:send_as_bot` (发送消息)
    *   `im:chat:read_as_bot` (获取群信息)
    *   `contact:user.id:read` (通过ID获取用户信息)

## 目录结构

```
.
├── app.py                  # 入口文件 (Flask Server)
├── config.py               # 配置加载
├── core/
│   ├── bot.py              # 飞书 Bot 交互逻辑
│   ├── llm.py              # LLM 交互逻辑
│   └── processor.py        # 消息处理核心业务
├── tests/                  # 单元测试
│   ├── test_bot.py
│   └── test_processor.py
├── requirements.txt
└── README.md
```
