import pytest
from sanic import Sanic
from sanic.response import text
from sanic.views import HTTPMethodView
from sanic.request import Request
from sanic.response import HTTPResponse

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
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_middleware(app):
    results = []

    @app.middleware("request")
    async def process_request(request):
        results.append(request)

    @app.middleware("response")
    async def process_response(request, response):
        results.append(request)
        results.append(response)

    request, response = app.test_client.get("/")
    
    assert response.text == "I am get method"
    assert type(results[0]) is Request
    assert isinstance(results[1], Request)
    assert isinstance(results[2], HTTPResponse)

def test_get_method_with_custom_header(app):
    request, response = app.test_client.get("/", headers={"Custom-Header": "Test"})
    assert response.text == "I am get method"
    assert response.status == 200
    assert response.headers.get("Custom-Header") is None  # No custom header in response

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/?param=value")
    assert response.text == "I am get method"
    assert response.status == 200