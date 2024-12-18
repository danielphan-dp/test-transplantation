import socket
import threading
import time
import pytest
from uvicorn.config import Config
from uvicorn.server import Server

calls = []

def test_shutdown(unused_tcp_port: int):
    class CustomServer(Server):
        def shutdown(self):
            calls.append('shutdown')
            super().shutdown()

    app = Response("Hello, world", media_type="text/plain")
    config = Config(app=app, port=unused_tcp_port)
    server = CustomServer(config=config)
    
    t = threading.Thread(target=server.run)
    t.daemon = True
    t.start()
    time.sleep(1)  # wait for server to start

    server.shutdown()
    assert 'shutdown' in calls

    server.should_exit = True
    t.join()