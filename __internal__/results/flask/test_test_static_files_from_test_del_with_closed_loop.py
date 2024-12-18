import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

def test_close_method(app):
    called = []
    
    class TestClient:
        def close(self):
            called.append(42)

    client = TestClient()
    client.close()
    
    assert called == [42]