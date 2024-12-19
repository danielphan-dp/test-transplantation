import asyncio
import pytest
from sanic import Sanic
from collections import namedtuple

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

def test_streaming_echo_empty_message():
    app = Sanic(name="Test")

    @app.post("/echo", stream=True)
    async def handler(request):
        res = await request.respond(content_type="text/plain; charset=utf-8")
        await res.send(end_stream=False)
        async for data in request.stream:
            await res.send(data.swapcase())
        await res.send(b"-", end_stream=True)

    async def client(app, reader, writer):
        host = "host: localhost:8000\r\n".encode()
        writer.write(
            b"POST /echo HTTP/1.1\r\n" + host + b"content-length: 0\r\n"
            b"content-type: text/plain; charset=utf-8\r\n"
            b"\r\n"
        )
        res = b""
        while b"\r\n\r\n" not in res:
            res += await reader.read(4096)
        assert res.startswith(b"HTTP/1.1 200 OK\r\n")
        assert res.endswith(b"\r\n\r\n")
        res = await read_chunk()
        assert res == b"-"

    async def read_chunk():
        buffer = b""
        while b"\r\n" not in buffer:
            data = await reader.read(4096)
            assert data
            buffer += data
        size, buffer = buffer.split(b"\r\n", 1)
        size = int(size, 16)
        if size == 0:
            return None
        while len(buffer) < size + 2:
            data = await reader.read(4096)
            assert data
            buffer += data
        assert buffer[size:size + 2] == b"\r\n"
        ret, buffer = buffer[:size], buffer[size + 2:]
        return ret

    app.run(access_log=False, single_process=True)

def test_streaming_echo_large_message():
    app = Sanic(name="Test")

    @app.post("/echo", stream=True)
    async def handler(request):
        res = await request.respond(content_type="text/plain; charset=utf-8")
        await res.send(end_stream=False)
        async for data in request.stream:
            await res.send(data.swapcase())
        await res.send(b"-", end_stream=True)

    async def client(app, reader, writer):
        message = b"a" * 10000  # Large message
        host = "host: localhost:8000\r\n".encode()
        writer.write(
            b"POST /echo HTTP/1.1\r\n" + host + b"content-length: 10000\r\n"
            b"content-type: text/plain; charset=utf-8\r\n"
            b"\r\n" + message
        )
        res = b""
        while b"\r\n\r\n" not in res:
            res += await reader.read(4096)
        assert res.startswith(b"HTTP/1.1 200 OK\r\n")
        assert res.endswith(b"\r\n\r\n")
        buffer = b""
        while True:
            chunk = await read_chunk()
            if chunk is None:
                break
            assert chunk == message.swapcase()

    async def read_chunk():
        buffer = b""
        while b"\r\n" not in buffer:
            data = await reader.read(4096)
            assert data
            buffer += data
        size, buffer = buffer.split(b"\r\n", 1)
        size = int(size, 16)
        if size == 0:
            return None
        while len(buffer) < size + 2:
            data = await reader.read(4096)
            assert data
            buffer += data
        assert buffer[size:size + 2] == b"\r\n"
        ret, buffer = buffer[:size], buffer[size + 2:]
        return ret

    app.run(access_log=False, single_process=True)