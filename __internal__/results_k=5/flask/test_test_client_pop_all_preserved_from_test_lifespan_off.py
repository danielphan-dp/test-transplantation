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
        assert response.is_streamed is False

def test_client_close_multiple_times(app, client):
    with client:
        response = client.get("/")
        response.close()
        with pytest.raises(RuntimeError):
            response.close()

def test_client_close_no_context(app, client):
    with pytest.raises(RuntimeError):
        client.close()