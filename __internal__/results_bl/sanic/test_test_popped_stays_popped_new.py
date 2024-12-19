import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.route("/get")
async def get_handler(request):
    return text('I am get method')

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_params(app):
    request, response = app.test_client.get("/get", params=[("param1", "value1")])
    assert response.status == 200
    assert response.text == 'I am get method'
    assert request.args.pop("param1") == ["value1"]
    assert "param1" not in request.args

def test_get_method_no_params(app):
    request, response = app.test_client.get("/get", params=[])
    assert response.status == 200
    assert response.text == 'I am get method'
    assert len(request.args) == 0

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404