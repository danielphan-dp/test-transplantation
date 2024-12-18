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
    ({"title": ""}, 400),
    ({"title": "Valid Title"}, 200)
])
def test_create_endpoint(app, client, data, expected_status):
    response = client.post("/create", json=data)
    assert response.status_code == expected_status

@pytest.mark.parametrize("debug", [True, False])
def test_create_debug_message(app, client, debug):
    app.config["DEBUG"] = debug
    rv = client.post("/create", data=None, content_type="application/json")
    assert rv.status_code == 400
    contains = b"Failed to decode JSON object" in rv.data
    assert contains == debug