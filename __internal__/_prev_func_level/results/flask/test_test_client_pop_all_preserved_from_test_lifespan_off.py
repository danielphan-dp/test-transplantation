import pytest
from flask import Flask, stream_with_context

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_client_close_context(app, client):
    @app.route("/")
    def index():
        return stream_with_context("hello")

    with client:
        rv = client.get("/")
    
    rv.close()
    
    # Check if the context is properly closed
    assert _cv_request.get(None) is None

def test_client_close_multiple_times(app, client):
    @app.route("/")
    def index():
        return stream_with_context("hello")

    with client:
        rv = client.get("/")
    
    rv.close()
    rv.close()  # Closing again to check for any errors

    assert _cv_request.get(None) is None

def test_client_close_with_no_context(app, client):
    with pytest.raises(RuntimeError):
        rv = client.get("/")
        rv.close()  # Attempting to close without a valid context should raise an error