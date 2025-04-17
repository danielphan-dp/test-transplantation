import pytest

@pytest.mark.parametrize('listener_name', AVAILABLE_LISTENERS)
def test_multiple_listeners(app, listener_name):
    """Test that multiple listeners work correctly"""
    output = []
    # Register multiple listeners
    for name in AVAILABLE_LISTENERS:
        app.listener(name)(create_listener(name, output))
    start_stop_app(app)
    for name in AVAILABLE_LISTENERS:
        assert app.name + name == output.pop()

@pytest.mark.parametrize('listener_name', AVAILABLE_LISTENERS)
@pytest.mark.asyncio
async def test_listener_with_async(app, listener_name):
    """Test that async listeners work correctly"""
    output = []
    app.listener(listener_name)(create_listener(listener_name, output))
    await start_stop_app(app)
    assert app.name + listener_name == output.pop()

@pytest.mark.parametrize('listener_name', AVAILABLE_LISTENERS)
def test_listener_order(app, listener_name):
    """Test that the order of listeners is preserved"""
    output = []
    app.listener(listener_name)(create_listener(listener_name, output))
    app.listener("another_listener")(create_listener("another_listener", output))
    start_stop_app(app)
    assert app.name + "another_listener" == output.pop()
    assert app.name + listener_name == output.pop()