import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method(app):
    @app.route("/post", methods=["POST"])
    async def handler(request):
        return text('I am post method')

    request, response = app.test_client.post("/post")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_not_allowed(app):
    @app.route("/post", methods=["GET"])
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/post")
    assert response.status == 200
    assert response.text == 'I am get method'

    request, response = app.test_client.post("/post")
    assert response.status == 405

def test_post_method_with_invalid_route(app):
    request, response = app.test_client.post("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_post_method_with_empty_body(app):
    @app.route("/post", methods=["POST"])
    async def handler(request):
        return text('Received empty body')

    request, response = app.test_client.post("/post", data="")
    assert response.status == 200
    assert response.text == 'Received empty body'