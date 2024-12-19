import pytest
from sanic.blueprints import Blueprint
from sanic.response import text
from sanic.views import HTTPMethodView

def test_get_method_response(app):
    bp = Blueprint("test_get_method", url_prefix="/test2")

    class TestView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    bp.add_route(TestView.as_view(), "/")
    app.blueprint(bp)
    request, response = app.test_client.get("/test2/")
    
    assert response.text == "I am get method"

def test_get_method_empty_request(app):
    bp = Blueprint("test_get_method_empty", url_prefix="/test3")

    class TestView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    bp.add_route(TestView.as_view(), "/")
    app.blueprint(bp)
    request, response = app.test_client.get("/test3/")
    
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    bp = Blueprint("test_get_method_invalid", url_prefix="/test4")

    class TestView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    bp.add_route(TestView.as_view(), "/")
    app.blueprint(bp)
    request, response = app.test_client.get("/test4/invalid")
    
    assert response.status == 404

def test_get_method_with_query_params(app):
    bp = Blueprint("test_get_method_query", url_prefix="/test5")

    class TestView(HTTPMethodView):
        def get(self, request):
            return text("I am get method with query params")

    bp.add_route(TestView.as_view(), "/")
    app.blueprint(bp)
    request, response = app.test_client.get("/test5/?param=value")
    
    assert response.text == "I am get method with query params"