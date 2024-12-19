import pytest
from sanic import Sanic
from sanic.exceptions import PayloadTooLarge
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method_with_large_payload(app):
    app.config.REQUEST_MAX_SIZE = 500

    @app.post("/post")
    async def post_handler(request):
        return text('I am post method')

    data = "b" * 1000
    _, response = app.test_client.post("/post", gather_request=False, data=data)
    assert response.status == 413
    assert "Request body" in response.text

def test_post_method_with_valid_payload(app):
    app.config.REQUEST_MAX_SIZE = 500

    @app.post("/post")
    async def post_handler(request):
        return text('I am post method')

    data = "valid data"
    _, response = app.test_client.post("/post", gather_request=False, data=data)
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_with_empty_payload(app):
    app.config.REQUEST_MAX_SIZE = 500

    @app.post("/post")
    async def post_handler(request):
        return text('I am post method')

    data = ""
    _, response = app.test_client.post("/post", gather_request=False, data=data)
    assert response.status == 200
    assert response.text == 'I am post method'