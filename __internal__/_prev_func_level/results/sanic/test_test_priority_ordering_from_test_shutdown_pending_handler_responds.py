import asyncio
import signal
import socket
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

    async def shutdown(app):
        await asyncio.sleep(1.1)
        app.stop()

    app.after_server_start(shutdown)

    try:
        app.run(HOST, get_port(), single_process=True)
    except KeyboardInterrupt:
        pass

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
async def test_start_stop_app_with_interrupt(app):
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

    async def shutdown(app):
        await asyncio.sleep(1.1)
        app.stop()

    app.after_server_start(shutdown)

    with pytest.raises(KeyboardInterrupt):
        app.run(HOST, get_port(), single_process=True)

    assert output == [
        "third",
        "bp_third",
        "second",
        "bp_second",
        "first",
        "fourth",
        "bp_first",
    ]