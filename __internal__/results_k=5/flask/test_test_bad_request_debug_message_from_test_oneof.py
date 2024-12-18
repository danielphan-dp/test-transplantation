import pytest
from flask import Flask, request

@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route("/create", methods=["POST"])
    def post():
        return 'Create'

    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.mark.parametrize("data, expected_status", [
    (None, 400),
    ({"title": "Test Title"}, 200),
    ({"title": ""}, 400),
    ({"title": "Valid Title"}, 200),
])
def test_post_create(client, data, expected_status):
    rv = client.post("/create", json=data)
    assert rv.status_code == expected_status

    if expected_status == 200:
        assert rv.data == b'Create'
    elif expected_status == 400:
        assert b"Title is required." in rv.data or b"Failed to decode JSON object" in rv.data