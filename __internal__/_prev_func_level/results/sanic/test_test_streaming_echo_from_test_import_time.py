import asyncio
import pytest
from sanic import Sanic, text
from sanic_testing.reusable import ReusableClient
from collections import namedtuple

@pytest.fixture
def test_app(app: Sanic):
    @app.post("/echo", stream=True)
    async def handler(request):
        res = await request.respond(content_type="text/plain; charset=utf-8")
        await res.send(end_stream=False)
        async for data in request.stream:
            await res.send(data.swapcase())
        await res.send(b"-", end_stream=True)

    return app

@pytest.fixture
def runner(test_app: Sanic, port):
    client = ReusableClient(test_app, port=port)
    client.run()
    yield client
    client.stop()

@pytest.fixture
def client(runner: ReusableClient):
    client = namedtuple("Client", ("raw", "send", "recv"))
    raw = RawClient(runner.host, runner.port)
    runner._run(raw.connect())

    def send(msg):
        nonlocal runner
        nonlocal raw
        runner._run(raw.send(msg))

    def recv(**kwargs):
        nonlocal runner
        nonlocal raw
        method = raw.recv_until if "until" in kwargs else raw.recv
        return runner._run(method(**kwargs))

    yield client(raw, send, recv)
    runner._run(raw.close())

@pytest.mark.parametrize("input_data, expected_output", [
    (b"a", b"A"),
    (b"b", b"B"),
    (b"c", b"C"),
    (b"ABCD", b"abcd"),
])
async def test_streaming_echo_with_various_inputs(client, input_data, expected_output):
    client.send(
        f"POST /echo HTTP/1.1\r\nhost: localhost:8000\r\ncontent-length: {len(input_data)}\r\ncontent-type: text/plain; charset=utf-8\r\n\r\n".encode()
    )
    client.send(input_data)
    response = client.recv()
    assert response == expected_output

async def test_streaming_echo_end_of_stream(client):
    client.send(
        b"POST /echo HTTP/1.1\r\nhost: localhost:8000\r\ncontent-length: 0\r\ncontent-type: text/plain; charset=utf-8\r\n\r\n"
    )
    response = client.recv()
    assert response == b"-"

async def test_streaming_echo_no_data(client):
    client.send(
        b"POST /echo HTTP/1.1\r\nhost: localhost:8000\r\ncontent-length: 0\r\ncontent-type: text/plain; charset=utf-8\r\n\r\n"
    )
    response = client.recv()
    assert response == b"-"