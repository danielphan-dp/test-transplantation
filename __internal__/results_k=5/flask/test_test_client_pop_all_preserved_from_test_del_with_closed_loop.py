import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_client_close_context(app, client):
    with client:
        response = client.get("/")
        response.close()
        assert response.status_code == 200

def test_client_close_multiple_times(app, client):
    with client:
        response = client.get("/")
        response.close()
        response.close()  # Closing again should not raise an error
        assert response.status_code == 200

def test_client_close_no_context(app, client):
    with pytest.raises(RuntimeError):
        client.close()  # Attempting to close without an active context

def test_client_close_preserves_context(app, client):
    with client:
        response = client.get("/")
        response.close()
        assert _cv_request.get(None) is not None  # Ensure context is preserved after close

def test_client_close_with_assertion(app, client):
    called = []
    def mock_close():
        called.append(42)

    client.close = mock_close
    with client:
        response = client.get("/")
    response.close()
    assert called == [42]  # Ensure close was called and recorded