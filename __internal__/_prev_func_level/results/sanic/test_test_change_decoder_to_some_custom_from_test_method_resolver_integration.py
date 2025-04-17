import json
import pytest
from sanic import Sanic, Request, text

def test_post_method_response():
    app = Sanic("TestApp")

    @app.post("/post")
    def post_handler(request):
        return text('I am post method')

    client = app.test_client()

    # Test valid POST request
    request, response = client.post("/post")
    assert response.text == 'I am post method'
    assert response.status == 200

    # Test POST request with additional data
    request, response = client.post("/post", json={"key": "value"})
    assert response.text == 'I am post method'
    assert response.status == 200

    # Test POST request with invalid endpoint
    request, response = client.post("/invalid")
    assert response.status == 404

    # Test POST request with wrong method
    request, response = client.get("/post")
    assert response.status == 405
    assert "Method GET not allowed for URL /post" in response.text

    # Test POST request with empty body
    request, response = client.post("/post", data={})
    assert response.text == 'I am post method'
    assert response.status == 200