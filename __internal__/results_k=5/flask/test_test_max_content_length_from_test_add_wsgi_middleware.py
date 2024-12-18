import pytest
from flask import Flask, request
from flask.testing import FlaskClient

@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 50

    @app.post("/")
    def index():
        return 'Create'

    @app.errorhandler(413)
    def catcher(error):
        return "42"

    return app

def test_post_create(client: FlaskClient) -> None:
    rv = client.post("/", data={"myfile": "foo"})
    assert rv.data == b'Create'

def test_post_max_content_length(client: FlaskClient) -> None:
    rv = client.post("/", data={"myfile": "foo" * 50})
    assert rv.data == b"42"

def test_post_empty_data(client: FlaskClient) -> None:
    rv = client.post("/", data={})
    assert rv.data == b'Create'

def test_post_large_data(client: FlaskClient) -> None:
    rv = client.post("/", data={"myfile": "a" * 51})
    assert rv.data == b"42"