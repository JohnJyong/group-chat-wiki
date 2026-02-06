import pytest
from unittest.mock import MagicMock, patch
from core.processor import MessageProcessor

@pytest.fixture
def processor():
    with patch('core.processor.FeishuBot') as MockBot, \
         patch('core.processor.LLMService') as MockLLM:
        proc = MessageProcessor()
        proc.bot = MockBot.return_value
        proc.llm = MockLLM.return_value
        yield proc

def test_handle_personal_summary_trigger(processor):
    # Setup Event Mock
    mock_event = MagicMock()
    mock_event.message.content = '{"text": "@Bot 跟我有关的事情"}'
    mock_event.message.chat_id = "oc_123"
    mock_event.message.message_id = "om_123"
    mock_event.sender.sender_id.open_id = "ou_user"

    # Setup Bot/LLM returns
    processor.bot.get_user_name.return_value = "Test User"
    processor.bot.get_chat_history.return_value = ["msg1", "msg2"]
    processor.llm.generate_personal_summary.return_value = "Summary"

    # Run
    processor.handle_im_message_receive_v1(mock_event)

    # Verify
    processor.bot.get_user_name.assert_called_with("ou_user")
    processor.bot.get_chat_history.assert_called_with("oc_123", limit=50)
    processor.llm.generate_personal_summary.assert_called_with("Test User", "msg1\nmsg2")
    processor.bot.reply_text.assert_called_with("om_123", "Summary")

def test_ignore_irrelevant_message(processor):
    # Setup Event Mock
    mock_event = MagicMock()
    mock_event.message.content = '{"text": "Hello World"}'
    
    # Run
    processor.handle_im_message_receive_v1(mock_event)

    # Verify NO calls
    processor.bot.get_user_name.assert_not_called()
