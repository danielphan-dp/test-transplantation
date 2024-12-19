import pytest
from sanic import Sanic
from sanic_testing import HOST

@pytest.mark.parametrize('listener_name', AVAILABLE_LISTENERS)
@pytest.mark.asyncio
async def test_listener_with_empty_list(app, listener_name):
    """Test that listener works with an empty list"""
    output = []
    app.listener(listener_name)(create_listener(listener_name, output))
    await start_stop_app(app)
    assert output == [app.name + listener_name]

@pytest.mark.parametrize('listener_name', AVAILABLE_LISTENERS)
@pytest.mark.asyncio
async def test_listener_with_existing_items(app, listener_name):
    """Test that listener correctly adds to a non-empty list"""
    output = ['existing_item']
    app.listener(listener_name)(create_listener(listener_name, output))
    await start_stop_app(app)
    assert output == [app.name + listener_name, 'existing_item']

@pytest.mark.parametrize('listener_name', AVAILABLE_LISTENERS)
@pytest.mark.asyncio
async def test_listener_with_multiple_calls(app, listener_name):
    """Test that multiple calls to the listener work correctly"""
    output = []
    app.listener(listener_name)(create_listener(listener_name, output))
    await start_stop_app(app)
    await start_stop_app(app)  # Call it again to test multiple invocations
    assert output == [app.name + listener_name, app.name + listener_name]

@pytest.mark.parametrize('listener_name', AVAILABLE_LISTENERS)
@pytest.mark.asyncio
async def test_listener_with_different_app_names(app, listener_name):
    """Test that listener works with different app names"""
    app2 = Sanic("AnotherApp")
    output = []
    app.listener(listener_name)(create_listener(listener_name, output))
    app2.listener(listener_name)(create_listener(listener_name, output))
    await start_stop_app(app)
    await start_stop_app(app2)
    assert output == [app.name + listener_name, app2.name + listener_name]