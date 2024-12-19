import asyncio
import pytest
from sanic import Sanic, Blueprint
from sanic_testing.testing import HOST
from conftest import get_port

@pytest.mark.asyncio
async def test_start_stop_app(app):
    output = []
    bp = Blueprint("bp")

    @app.before_server_start
    async def first(app):
        output.append("first")

    @app.listener("before_server_start", priority=2)
    async def second(app):
        output.append("second")

    @app.before_server_start(priority=3)
    async def third(app):
        output.append("third")

    @bp.before_server_start
    async def bp_first(app):
        output.append("bp_first")

    @bp.listener("before_server_start", priority=2)
    async def bp_second(app):
        output.append("bp_second")

    @bp.before_server_start(priority=3)
    async def bp_third(app):
        output.append("bp_third")

    @app.before_server_start
    async def fourth(app):
        output.append("fourth")

    app.blueprint(bp)

    # Start the app and ensure it stops after a delay
    await asyncio.sleep(0.1)  # Allow some time for the app to start
    start_stop_app(app)

    # Check the order of the listeners
    assert output == [
        "third",
        "bp_third",
        "second",
        "bp_second",
        "first",
        "fourth",
        "bp_first",
    ]

@pytest.mark.asyncio
async def test_start_stop_app_keyboard_interrupt(app):
    output = []
    bp = Blueprint("bp")

    @app.before_server_start
    async def first(app):
        output.append("first")

    @app.listener("before_server_start", priority=2)
    async def second(app):
        output.append("second")

    @app.before_server_start(priority=3)
    async def third(app):
        output.append("third")

    app.blueprint(bp)

    # Simulate a keyboard interrupt
    with pytest.raises(KeyboardInterrupt):
        start_stop_app(app)

    assert output == [
        "third",
        "second",
        "first",
    ]