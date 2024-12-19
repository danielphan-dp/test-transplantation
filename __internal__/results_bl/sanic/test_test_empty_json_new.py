import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.route("/get")
    async def get_handler(request):
        return text('I am get method')
    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.body == b'I am get method'

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.body == b'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.body == b'I am get method'