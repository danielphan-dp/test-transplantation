import pytest
from sanic import Sanic
from sanic.response import text
from sanic.views import HTTPMethodView

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    app.add_route(TestView.as_view(), "/test")

    request, response = app.test_client.get("/test")
    assert response.text == "I am get method"

def test_get_method_with_empty_response(app):
    class EmptyView(HTTPMethodView):
        def get(self, request):
            return text("")

    app.add_route(EmptyView.as_view(), "/empty")

    request, response = app.test_client.get("/empty")
    assert response.text == ""

def test_get_method_with_different_response(app):
    class DifferentResponseView(HTTPMethodView):
        def get(self, request):
            return text("Different response")

    app.add_route(DifferentResponseView.as_view(), "/different")

    request, response = app.test_client.get("/different")
    assert response.text == "Different response"

def test_get_method_with_status_code(app):
    class StatusView(HTTPMethodView):
        def get(self, request):
            return text("Status 204", status=204)

    app.add_route(StatusView.as_view(), "/status")

    request, response = app.test_client.get("/status")
    assert response.status == 204
    assert response.text == "Status 204"