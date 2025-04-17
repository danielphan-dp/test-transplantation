import pytest
from sanic import Sanic, Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/get")

    _, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    _, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_query_param(app):
    class DummyView:
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f'Param is {param}')

    app.add_route(DummyView().get, "/get_with_param")

    _, response = app.test_client.get("/get_with_param?param=test")
    assert response.text == "Param is test"

    _, response = app.test_client.get("/get_with_param")
    assert response.text == "Param is default"

def test_get_method_with_invalid_method(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/get")

    _, response = app.test_client.post("/get")
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text

def test_get_method_with_headers(app):
    class DummyView:
        def get(self, request):
            return text('I am get method with headers')

    app.add_route(DummyView().get, "/get_with_headers")

    _, response = app.test_client.get("/get_with_headers", headers={"Custom-Header": "value"})
    assert response.text == "I am get method with headers"
    assert response.status == 200

def test_get_method_response_type(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/get_response_type")

    _, response = app.test_client.get("/get_response_type")
    assert isinstance(response, text)  # Ensure the response is of type text
    assert response.text == "I am get method"