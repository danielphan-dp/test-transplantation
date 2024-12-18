import pytest
from flask import Flask, stream_with_context
from flask.globals import _cv_request

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
    assert _cv_request.get(None) is None

def test_client_close_multiple_calls(app, client):
    @app.route("/")
    def index():
        return stream_with_context("hello")

    with client:
        rv1 = client.get("/")
        rv2 = client.get("/")
    
    rv1.close()
    rv2.close()
    assert _cv_request.get(None) is None

def test_client_close_no_context(app, client):
    with client:
        rv = client.get("/")
    
    rv.close()
    assert _cv_request.get(None) is None

def test_client_close_after_request(app, client):
    @app.route("/")
    def index():
        return stream_with_context("hello")

    with client:
        rv = client.get("/")
    
    rv.close()
    assert _cv_request.get(None) is None

def test_client_close_with_error(app, client):
    @app.route("/")
    def index():
        raise Exception("Test Exception")

    with pytest.raises(Exception):
        with client:
            rv = client.get("/")
    
    assert _cv_request.get(None) is None