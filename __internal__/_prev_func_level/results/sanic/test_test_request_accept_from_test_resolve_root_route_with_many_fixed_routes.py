import uuid
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView.get, "/")

    request, response = app.test_client.get("/")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_custom_header(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView.get, "/")

    request, response = app.test_client.get("/", headers={"Custom-Header": "value"})
    assert response.text == "I am get method"
    assert response.status == 200
    assert request.headers.get("Custom-Header") == "value"

def test_get_method_with_invalid_route(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView.get, "/valid")

    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(app):
    class DummyView:
        def get(self, request):
            return text(f"I am get method with query param: {request.args.get('param')}")

    app.add_route(DummyView.get, "/")

    request, response = app.test_client.get("/?param=test")
    assert response.text == "I am get method with query param: test"
    assert response.status == 200

def test_get_method_with_multiple_queries(app):
    class DummyView:
        def get(self, request):
            return text(f"Params: {', '.join(f'{k}={v[0]}' for k, v in request.args.items())}")

    app.add_route(DummyView.get, "/")

    request, response = app.test_client.get("/?param1=value1&param2=value2")
    assert response.text == "Params: param1=value1, param2=value2"
    assert response.status == 200