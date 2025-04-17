import pytest
from sanic import Sanic
from sanic_testing.testing import HOST
from sanic.exceptions import BadRequest

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@pytest.mark.asyncio
async def test_create_listener_inserts_correctly(app):
    output = []
    listener_name = "test_listener"
    listener = create_listener(listener_name, output)
    
    await listener(app, None)  # Simulating the app and loop parameters
    assert output[0] == app.name + listener_name

@pytest.mark.asyncio
async def test_create_listener_multiple_inserts(app):
    output = []
    listener_names = ["listener_one", "listener_two", "listener_three"]
    
    for name in listener_names:
        listener = create_listener(name, output)
        await listener(app, None)
    
    assert output[0] == app.name + listener_names[2]
    assert output[1] == app.name + listener_names[1]
    assert output[2] == app.name + listener_names[0]

@pytest.mark.asyncio
async def test_create_listener_with_empty_list(app):
    output = []
    listener_name = "empty_listener"
    listener = create_listener(listener_name, output)
    
    await listener(app, None)
    assert len(output) == 1
    assert output[0] == app.name + listener_name

@pytest.mark.asyncio
async def test_create_listener_no_app_name(app):
    app.name = ""
    output = []
    listener_name = "no_name_listener"
    listener = create_listener(listener_name, output)
    
    await listener(app, None)
    assert output[0] == listener_name  # Expecting just the listener name since app.name is empty

@pytest.mark.asyncio
async def test_create_listener_with_none_app(app):
    output = []
    listener_name = "none_app_listener"
    listener = create_listener(listener_name, output)
    
    with pytest.raises(TypeError):
        await listener(None, None)  # Passing None as app should raise an error