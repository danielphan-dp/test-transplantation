import pytest
from flask import Flask, request

def test_post_method(client):
    app = Flask(__name__)

    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    with app.test_request_context():
        response = client.post("/create")
        assert response.data == b'Create'

def test_post_method_with_data(client):
    app = Flask(__name__)

    @app.route("/create", methods=["POST"])
    def create():
        return request.form.get("status", "Create")

    response = client.post("/create", data={"status": "success"})
    assert response.data == b'success'

def test_post_method_with_empty_data(client):
    app = Flask(__name__)

    @app.route("/create", methods=["POST"])
    def create():
        return request.form.get("status", "Create")

    response = client.post("/create", data={})
    assert response.data == b'Create'

def test_post_method_invalid_route(client):
    response = client.post("/invalid")
    assert response.status_code == 404