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

    app.add_route(GetView.as_view(), "/get_view")
    return app

def test_get_view(app):
    request, response = app.test_client.get("/get_view")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_view_not_found(app):
    request, response = app.test_client.get("/non_existent_route")
    assert response.status == 404
    assert "Requested URL /non_existent_route not found" in response.text

def test_get_view_method_not_allowed(app):
    request, response = app.test_client.post("/get_view")
    assert response.status == 405
    assert "Method POST not allowed for URL /get_view" in response.text

def test_get_view_empty_response(app):
    class EmptyView(HTTPMethodView):
        def get(self, request):
            return text("")

    app.add_route(EmptyView.as_view(), "/empty_view")
    request, response = app.test_client.get("/empty_view")
    assert response.status == 200
    assert response.text == ""