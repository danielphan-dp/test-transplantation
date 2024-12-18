import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/get")
    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_content_type(app):
    request, response = app.test_client.get("/get")
    assert response.headers.get("Content-Type") == "text/plain; charset=utf-8"

def test_get_method_empty_request(app):
    request, response = app.test_client.get("/get?param=")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_additional_params(app):
    request, response = app.test_client.get("/get?extra_param=value")
    assert response.status == 200
    assert response.text == "I am get method"