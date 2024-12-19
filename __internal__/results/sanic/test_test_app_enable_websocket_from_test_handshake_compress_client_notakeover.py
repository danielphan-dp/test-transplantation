import pytest

@pytest.mark.parametrize('websocket_enabled', [True, False])
@pytest.mark.parametrize('enable', [True, False])
@pytest.mark.asyncio
async def test_send_functionality(message_stack, websocket_enabled, enable):
    send_function = send(message_stack)
    
    # Simulate enabling the websocket
    message_stack.clear()
    
    if websocket_enabled:
        await send_function("Test message")
        assert message_stack == ["Test message"]
    else:
        await send_function("Test message")
        assert message_stack == []  # Expect no message to be sent if websocket is disabled

    # Test enabling and disabling the websocket
    if enable:
        websocket_enabled = True
    else:
        websocket_enabled = False

    assert websocket_enabled == enable
    if enable:
        await send_function("Another test message")
        assert message_stack == ["Test message", "Another test message"]
    else:
        await send_function("Another test message")
        assert message_stack == ["Test message"]  # Should not add the new message if disabled