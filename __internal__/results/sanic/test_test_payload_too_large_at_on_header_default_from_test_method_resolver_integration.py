import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_post_method_response(app):
    @app.post("/post")
    async def handler(request):
        return text("I am post method")

    request, response = app.test_client.post("/post")
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_with_large_payload(app):
    @app.post("/post")
    async def handler(request):
        return text("I am post method")

    data = "a" * 1000
    app.config.REQUEST_MAX_SIZE = 500
    _, response = app.test_client.post("/post", gather_request=False, data=data)
    assert response.status == 413
    assert "Request body" in response.text

def test_post_method_with_empty_payload(app):
    @app.post("/post")
    async def handler(request):
        return text("I am post method")

    request, response = app.test_client.post("/post", data="")
    assert response.status == 200
    assert response.text == "I am post method"