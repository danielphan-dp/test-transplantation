import asyncio
import pytest
from sanic import Sanic, Blueprint
from sanic_testing.testing import HOST
from conftest import get_port

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_start_stop_app_with_keyboard_interrupt(app):
    output = []
    
    @app.before_server_start
    async def first(app):
        output.append("first")

    @app.listener("before_server_start", priority=2)
    async def second(app):
        output.append("second")

    @app.before_server_start(priority=3)
    async def third(app):
        output.append("third")

    @app.before_server_start
    async def fourth(app):
        output.append("fourth")

    async def simulate_keyboard_interrupt():
        await asyncio.sleep(0.5)
        raise KeyboardInterrupt

    app.add_task(simulate_keyboard_interrupt())
    start_stop_app(app)

    assert output == ["third", "second", "first", "fourth"]

def test_start_stop_app_without_keyboard_interrupt(app):
    output = []
    
    @app.before_server_start
    async def first(app):
        output.append("first")

    @app.listener("before_server_start", priority=2)
    async def second(app):
        output.append("second")

    @app.before_server_start(priority=3)
    async def third(app):
        output.append("third")

    @app.before_server_start
    async def fourth(app):
        output.append("fourth")

    start_stop_app(app)

    assert output == ["third", "second", "first", "fourth"]

def test_start_stop_app_with_no_listeners(app):
    output = []

    start_stop_app(app)

    assert output == []  # No listeners should result in an empty output list.