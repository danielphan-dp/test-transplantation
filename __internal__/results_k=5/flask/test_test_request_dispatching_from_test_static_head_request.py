import pytest
import flask

@pytest.fixture
def app():
    app = flask.Flask(__name__)

    @app.route("/")
    def index():
        return flask.Response("", headers={"X-Method": "HEAD"})

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_head_request(client):
    rv = client.head("/")
    assert rv.status_code == 200
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"

def test_head_request_with_nonexistent_route(client):
    rv = client.head("/nonexistent")
    assert rv.status_code == 404

def test_head_request_on_post_route(client):
    @client.application.route("/post", methods=["POST"])
    def post_route():
        return "POST response"

    rv = client.head("/post")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["HEAD", "OPTIONS", "POST"]

def test_head_request_with_custom_header(client):
    @client.application.route("/custom", methods=["HEAD"])
    def custom_head():
        return flask.Response("", headers={"X-Custom-Header": "CustomValue"})

    rv = client.head("/custom")
    assert rv.status_code == 200
    assert rv.headers["X-Custom-Header"] == "CustomValue"