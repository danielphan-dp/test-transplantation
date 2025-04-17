import os
import pytest
from sanic import Sanic
from sanic.response import empty
from tests.client import RawClient

@pytest.fixture(autouse=True)
def reset():
    try:
        del os.environ['SANIC_MOTD_OUTPUT']
    except KeyError:
        pass

@pytest.mark.skipif(sys.version_info < (3, 9), reason='Not supported in 3.7')
async def test_http1_response_without_motd(port):
    Sanic._app_registry.clear()
    app = Sanic("TestNoMOTD")
    response = b""

    @app.get("/")
    async def handler(*_):
        return empty()

    @app.after_server_start
    async def do_request(*_):
        nonlocal response

        app.router.reset()
        app.router.finalize()

        client = RawClient(app.state.host, app.state.port)
        await client.connect()
        await client.send(
            """
            GET / HTTP/1.1
            host: localhost:7777

            """
        )
        response = await client.recv(1024)
        await client.close()

    @app.after_server_start
    def shutdown(*_):
        app.stop()

    app.prepare(version=1, port=port)
    Sanic.serve_single(app)

    assert b'alt-svc' not in response

@pytest.mark.skipif(sys.version_info < (3, 9), reason='Not supported in 3.7')
async def test_http1_response_with_motd(port):
    os.environ['SANIC_MOTD_OUTPUT'] = '1'
    Sanic._app_registry.clear()
    app = Sanic("TestWithMOTD")
    response = b""

    @app.get("/")
    async def handler(*_):
        return empty()

    @app.after_server_start
    async def do_request(*_):
        nonlocal response

        app.router.reset()
        app.router.finalize()

        client = RawClient(app.state.host, app.state.port)
        await client.connect()
        await client.send(
            """
            GET / HTTP/1.1
            host: localhost:7777

            """
        )
        response = await client.recv(1024)
        await client.close()

    @app.after_server_start
    def shutdown(*_):
        app.stop()

    app.prepare(version=1, port=port)
    Sanic.serve_single(app)

    assert b'alt-svc' in response

@pytest.mark.skipif(sys.version_info < (3, 9), reason='Not supported in 3.7')
async def test_http1_response_with_invalid_env_variable(port):
    os.environ['SANIC_MOTD_OUTPUT'] = 'invalid_value'
    Sanic._app_registry.clear()
    app = Sanic("TestInvalidMOTD")
    response = b""

    @app.get("/")
    async def handler(*_):
        return empty()

    @app.after_server_start
    async def do_request(*_):
        nonlocal response

        app.router.reset()
        app.router.finalize()

        client = RawClient(app.state.host, app.state.port)
        await client.connect()
        await client.send(
            """
            GET / HTTP/1.1
            host: localhost:7777

            """
        )
        response = await client.recv(1024)
        await client.close()

    @app.after_server_start
    def shutdown(*_):
        app.stop()

    app.prepare(version=1, port=port)
    Sanic.serve_single(app)

    assert b'alt-svc' not in response