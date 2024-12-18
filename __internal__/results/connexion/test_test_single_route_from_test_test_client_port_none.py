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
    post_response = app_client.post("/post", json={"key": "value"})
    assert post_response.status_code == 201
    assert post_response.json == {'key': 'value', 'name': 'post'}

    # Test post request with no body
    post_empty_response = app_client.post("/post")
    assert post_empty_response.status_code == 201
    assert post_empty_response.json == {'name': 'post'}

    # Test post request with unexpected data
    post_invalid_response = app_client.post("/post", json={"unexpected": "data"})
    assert post_invalid_response.status_code == 201
    assert post_invalid_response.json == {'unexpected': 'data', 'name': 'post'}

    # Test method not allowed for GET request
    get_response = app_client.get("/post")
    assert get_response.status_code == 405