import pytest
from unittest.mock import MagicMock, patch
from core.bot import FeishuBot

@pytest.fixture
def mock_lark_client():
    with patch('lark_oapi.Client.builder') as mock_builder:
        yield mock_builder.return_value.app_id.return_value.app_secret.return_value.build.return_value

def test_get_user_name_success(mock_lark_client):
    # Setup Mock
    mock_resp = MagicMock()
    mock_resp.success.return_value = True
    mock_resp.data.user.name = "Test User"
    mock_lark_client.contact.v3.user.get.return_value = mock_resp

    # Test
    bot = FeishuBot()
    name = bot.get_user_name("ou_123")
    
    assert name == "Test User"

def test_get_user_name_failure(mock_lark_client):
    # Setup Mock
    mock_resp = MagicMock()
    mock_resp.success.return_value = False
    mock_resp.code = 404
    mock_resp.msg = "Not Found"
    mock_lark_client.contact.v3.user.get.return_value = mock_resp

    # Test
    bot = FeishuBot()
    name = bot.get_user_name("ou_123")
    
    assert name == "Unknown User"
