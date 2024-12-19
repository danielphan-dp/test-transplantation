import pytest
from sanic import Sanic
from sanic.response import text
from sanic_routing.exceptions import RouteExists

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    with pytest.raises(RouteExists):
        @app.route("/get")
        def another_get_method(request):
            return text("Another get method")

def test_get_method_with_custom_header(app):
    request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_different_host(app):
    headers = {"Host": "different.com"}
    request, response = app.test_client.get("/get", headers=headers)
    assert response.text == "I am get method"