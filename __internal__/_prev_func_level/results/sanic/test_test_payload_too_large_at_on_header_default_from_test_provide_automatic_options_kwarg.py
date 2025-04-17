import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method_response(app):
    @app.post("/post")
    async def post_handler(request):
        return text('I am post method')

    request, response = app.test_client.post("/post")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_with_large_payload(app):
    @app.post("/post")
    async def post_handler(request):
        return text('I am post method')

    data = "a" * 1000
    app.config.REQUEST_MAX_SIZE = 500
    _, response = app.test_client.post("/post", gather_request=False, data=data)
    assert response.status == 413
    assert "Request body" in response.text

def test_post_method_invalid_route(app):
    request, response = app.test_client.post("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_post_method_with_options(app):
    @app.post("/post")
    async def post_handler(request):
        return text('I am post method')

    rv = app.test_client.options("/post")
    assert rv.status == 200
    assert 'POST' in rv.headers['Allow']