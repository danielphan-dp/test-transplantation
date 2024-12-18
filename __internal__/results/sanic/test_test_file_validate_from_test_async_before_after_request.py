import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.route("/get", methods=["GET"])
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app):
    @app.route("/get", methods=["GET"])
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_query_params(app):
    @app.route("/get", methods=["GET"])
    def get_method(request):
        param = request.args.get("param", "default")
        return text(f'Param value is {param}')

    request, response = app.test_client.get("/get?param=test")
    assert response.status == 200
    assert response.text == 'Param value is test'

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'Param value is default'