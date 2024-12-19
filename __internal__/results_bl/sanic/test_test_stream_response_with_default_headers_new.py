import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.route("/get")
async def get_method(request):
    return text('I am get method')

def test_get_method_response(app):
    _, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200
    assert response.headers["Content-Type"] == "text/plain; charset=utf-8"

def test_get_method_invalid_route(app):
    _, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(app):
    _, response = app.test_client.get("/get?param=value")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_with_headers(app):
    _, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.text == 'I am get method'
    assert response.status == 200
    assert response.headers["Custom-Header"] != "value"  # Custom header should not be in response