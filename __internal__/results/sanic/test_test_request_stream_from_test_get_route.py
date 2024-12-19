import asyncio
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.views import HTTPMethodView

@pytest.fixture
def app():
    app = Sanic("test_app")

    class GetView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    app.add_route(GetView.as_view(), "/get_method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get_method")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent")
    assert response.status == 404
    assert "Requested URL /non_existent not found" in response.text

def test_get_method_with_query_param(app):
    request, response = app.test_client.get("/get_method?param=test")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_method(app):
    request, response = app.test_client.post("/get_method")
    assert response.status == 405
    assert "Method POST not allowed for URL /get_method" in response.text