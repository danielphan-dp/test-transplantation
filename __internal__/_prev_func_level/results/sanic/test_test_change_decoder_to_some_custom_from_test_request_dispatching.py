import pytest
from sanic import Sanic, Request, text

@pytest.fixture
def app():
    return Sanic("TestApp")

def test_post_method_response(app):
    @app.post("/post")
    def post_handler(request):
        return text('I am post method')

    request, response = app.test_client.post("/post")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_with_data(app):
    @app.post("/post-data")
    def post_data_handler(request):
        return text(request.json)

    req_body = {"key": "value"}
    request, response = app.test_client.post("/post-data", json=req_body)
    assert response.status == 200
    assert response.text == '{"key": "value"}'

def test_post_method_invalid_route(app):
    request, response = app.test_client.post("/invalid-route")
    assert response.status == 404

def test_post_method_with_empty_body(app):
    @app.post("/post-empty")
    def post_empty_handler(request):
        return text('Received empty body')

    request, response = app.test_client.post("/post-empty", data={})
    assert response.status == 200
    assert response.text == 'Received empty body'