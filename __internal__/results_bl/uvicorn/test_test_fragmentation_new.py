import socket
import threading
import time
import pytest
from uvicorn.config import Config
from uvicorn.main import Server
from tests.response import Response

def test_shutdown(unused_tcp_port: int):
    calls = []

    class MockServer:
        def shutdown(self):
            calls.append('shutdown')

    app = Response("Hello, world", media_type="text/plain")
    config = Config(app=app, http="httptools", port=unused_tcp_port)
    server = MockServer()
    t = threading.Thread(target=server.shutdown)
    t.daemon = True
    t.start()
    time.sleep(1)  # wait for shutdown to be called

    assert 'shutdown' in calls
    server.shutdown()
    assert len(calls) == 1  # Ensure shutdown was called only once

    t.join()