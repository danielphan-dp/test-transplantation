import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.route("/get")
    async def get_method(request):
        return text('I am get method')

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.content_type == "text/plain; charset=utf-8"
    assert response.body == b'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.content_type == "text/plain; charset=utf-8"
    assert response.body == b'I am get method'