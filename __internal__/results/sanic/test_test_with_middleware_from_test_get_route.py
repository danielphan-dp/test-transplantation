import pytest
from sanic import Sanic
from sanic.response import text
from sanic.views import HTTPMethodView
from sanic.request import Request

@pytest.fixture
def app():
    app = Sanic("test_app")

    class DummyView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    app.add_route(DummyView.as_view(), "/")
    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/?param=value")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_middleware(app):
    results = []

    @app.middleware
    async def handler(request):
        results.append(request)

    request, response = app.test_client.get("/")
    assert response.text == "I am get method"
    assert type(results[0]) is Request

def test_get_method_response_content_type(app):
    request, response = app.test_client.get("/")
    assert response.content_type == "text/plain; charset=utf-8"