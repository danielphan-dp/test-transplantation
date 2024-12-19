import pytest
from sanic.blueprints import Blueprint
from sanic.response import text
from sanic.views import HTTPMethodView

def test_get_method_response(app):
    bp = Blueprint("test_get_method")

    class TestView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    TestView.attach(bp, "/test")
    app.blueprint(bp)
    request, response = app.test_client.get("/test")

    assert response.text == "I am get method"

def test_get_method_empty_request(app):
    bp = Blueprint("test_get_method_empty")

    class TestView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    TestView.attach(bp, "/empty")
    app.blueprint(bp)
    request, response = app.test_client.get("/empty")

    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")

    assert response.status == 404

def test_get_method_with_query_params(app):
    bp = Blueprint("test_get_method_query")

    class TestView(HTTPMethodView):
        def get(self, request):
            return text(f"Query param received: {request.args.get('param', 'none')}")

    TestView.attach(bp, "/query")
    app.blueprint(bp)
    request, response = app.test_client.get("/query?param=test")

    assert response.text == "Query param received: test"