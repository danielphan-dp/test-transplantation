import json
import unittest
from connexion import App

def test_post_method():
    app = App(__name__)

    @app.route("/post", methods=["POST"])
    def post_method(**kwargs):
        kwargs.update({'name': 'post'})
        return (kwargs, 201)

    app_client = app.test_client()

    # Test valid post request
    response = app_client.post("/post", json={"key": "value"})
    assert response.status_code == 201
    assert response.json == {'key': 'value', 'name': 'post'}

    # Test post request with no data
    response_no_data = app_client.post("/post")
    assert response_no_data.status_code == 201
    assert response_no_data.json == {'name': 'post'}

    # Test post request with unexpected data
    response_unexpected_data = app_client.post("/post", json={"unexpected": "data"})
    assert response_unexpected_data.status_code == 201
    assert response_unexpected_data.json == {'unexpected': 'data', 'name': 'post'}

    # Test post request with invalid JSON
    response_invalid_json = app_client.post("/post", data="invalid json")
    assert response_invalid_json.status_code == 400  # Assuming the app returns 400 for invalid JSON

    # Test method not allowed
    response_method_not_allowed = app_client.get("/post")
    assert response_method_not_allowed.status_code == 405