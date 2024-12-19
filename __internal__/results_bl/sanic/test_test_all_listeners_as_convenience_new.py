import asyncio
import pytest
from sanic import Sanic
from sanic_testing.testing import HOST
from sanic.exceptions import SanicException

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@pytest.mark.asyncio
async def test_create_listener_with_empty_list(app):
    output = []
    listener_name = "test_listener"
    listener = create_listener(listener_name, output)
    await listener(app, asyncio.get_event_loop())
    assert output == [app.name + listener_name]

@pytest.mark.asyncio
async def test_create_listener_with_existing_items(app):
    output = ["existing_item"]
    listener_name = "test_listener"
    listener = create_listener(listener_name, output)
    await listener(app, asyncio.get_event_loop())
    assert output == [app.name + listener_name, "existing_item"]

@pytest.mark.asyncio
async def test_create_listener_multiple_calls(app):
    output = []
    listener_names = ["listener_one", "listener_two"]
    for listener_name in listener_names:
        listener = create_listener(listener_name, output)
        await listener(app, asyncio.get_event_loop())
    assert output == [app.name + "listener_two", app.name + "listener_one"]

@pytest.mark.asyncio
async def test_create_listener_with_non_string_listener_name(app):
    output = []
    listener_name = 12345
    listener = create_listener(listener_name, output)
    with pytest.raises(TypeError):
        await listener(app, asyncio.get_event_loop())