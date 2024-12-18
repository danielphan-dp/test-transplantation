import pytest
from flask import Flask, request

@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    return app

@pytest.mark.parametrize("data, expected_status", [
    (None, 400),
    ({"title": "Test Title"}, 200),
    ({"title": ""}, 400),
])
def test_create_endpoint(app, client, data, expected_status):
    response = client.post("/create", json=data)
    assert response.status_code == expected_status

    if expected_status == 400:
        assert b"Title is required." in response.data or b"Failed to decode JSON object" in response.data
    elif expected_status == 200:
        assert response.data == b'Create'