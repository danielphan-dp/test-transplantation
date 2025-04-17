import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('data, expected_response', [
    ({"key": "value"}, "I am post method"),
    ({"key": ""}, "I am post method"),
    (None, "I am post method"),
])
def test_post_method(app, data, expected_response):
    @app.post("/post")
    async def post_method(request):
        return text('I am post method')

    request, response = app.test_client.post("/post", json=data)
    assert response.status == 200
    assert response.text == expected_response

def test_post_method_invalid_content_type(app):
    @app.post("/post")
    async def post_method(request):
        return text('I am post method')

    request, response = app.test_client.post("/post", data="Invalid data", content_type="text/plain")
    assert response.status == 415  # Unsupported Media Type

def test_post_method_not_found(app):
    request, response = app.test_client.post("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_post_method_method_not_allowed(app):
    @app.post("/post")
    async def post_method(request):
        return text('I am post method')

    request, response = app.test_client.get("/post")
    assert response.status == 405
    assert "Method GET not allowed for URL /post" in response.text