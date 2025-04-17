import pytest
from sanic import Sanic, Request, json, text

@pytest.fixture
def app():
    return Sanic("TestApp")

def test_post_method_response(app):
    @app.post("/post")
    def post_handler(request):
        return text('I am post method')

    request, response = app.test_client.post("/post")
    assert response.text == 'I am post method'

def test_post_method_with_data(app):
    @app.post("/post-data")
    def post_data_handler(request):
        return json(request.json)

    req_body = {"key": "value"}
    request, response = app.test_client.post("/post-data", json=req_body)
    assert response.json == req_body

def test_post_method_empty_body(app):
    @app.post("/post-empty")
    def post_empty_handler(request):
        return text('Received empty body')

    request, response = app.test_client.post("/post-empty", data="")
    assert response.text == 'Received empty body'

def test_post_method_invalid_route(app):
    request, response = app.test_client.post("/invalid-route")
    assert response.status == 404
    assert "Requested URL /invalid-route not found" in response.text

def test_post_method_with_custom_header(app):
    @app.post("/post-header")
    def post_header_handler(request):
        return text(request.headers.get('X-Custom-Header', 'No Header'))

    request, response = app.test_client.post("/post-header", headers={'X-Custom-Header': 'HeaderValue'})
    assert response.text == 'HeaderValue'