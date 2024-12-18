import pytest
from flask import Flask

def test_post_method(client):
    app = Flask(__name__)

    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    with app.test_request_context():
        response = client.post("/create")
        assert response.data.decode() == 'Create'
        assert response.status_code == 200

    with app.test_request_context():
        response = client.post("/create", data={"foo": "bar"})
        assert response.data.decode() == 'Create'
        assert response.status_code == 200

    with app.test_request_context():
        response = client.post("/create", data={})
        assert response.data.decode() == 'Create'
        assert response.status_code == 200