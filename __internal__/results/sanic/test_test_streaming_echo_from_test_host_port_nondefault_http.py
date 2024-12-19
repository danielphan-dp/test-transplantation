import asyncio
import pytest
from sanic import Sanic, text

@pytest.fixture
def test_app():
    app = Sanic(name="Test")
    
    @app.post("/echo", stream=True)
    async def handler(request):
        res = await request.respond(content_type="text/plain; charset=utf-8")
        await res.send(end_stream=False)
        async for data in request.stream:
            await res.send(data.swapcase())
        await res.send(b"-", end_stream=True)

    return app

@pytest.fixture
def runner(test_app):
    client = ReusableClient(test_app, port=8000)
    client.run()
    yield client
    client.stop()

@pytest.fixture
def client(runner):
    client = namedtuple('Client', ('raw', 'send', 'recv'))
    raw = RawClient(runner.host, runner.port)
    runner._run(raw.connect())

    def send(msg):
        nonlocal runner
        nonlocal raw
        runner._run(raw.send(msg))

    def recv(**kwargs):
        nonlocal runner
        nonlocal raw
        method = raw.recv_until if 'until' in kwargs else raw.recv
        return runner._run(method(**kwargs))
    
    yield client(raw, send, recv)
    runner._run(raw.close())

def test_streaming_echo_empty_message(client):
    client.send(b"")
    res = client.recv()
    assert res == b"-"

def test_streaming_echo_uppercase(client):
    client.send(b"HELLO")
    res = client.recv()
    assert res == b"hello"

def test_streaming_echo_mixed_case(client):
    client.send(b"Hello World")
    res = client.recv()
    assert res == b"hELLO wORLD"

def test_streaming_echo_multiple_messages(client):
    client.send(b"a")
    res = client.recv()
    assert res == b"A"
    
    client.send(b"b")
    res = client.recv()
    assert res == b"B"
    
    client.send(b"c")
    res = client.recv()
    assert res == b"C"
    
    res = client.recv()
    assert res == b"-"

def test_streaming_echo_end_of_stream(client):
    client.send(b"xyz")
    res = client.recv()
    assert res == b"XYZ"
    
    res = client.recv()
    assert res == b"-"
    
    res = client.recv()
    assert res is None