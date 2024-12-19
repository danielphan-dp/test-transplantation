import pytest
from sanic.blueprints import Blueprint
from sanic.response import text
from sanic.views import HTTPMethodView

def test_get_method_empty_request(app):
    bp = Blueprint("test_text_empty_request")

    class DummyView(HTTPMethodView, attach=bp, uri="/empty"):
        def get(self, request):
            return text("I am get method")

    app.blueprint(bp)
    request, response = app.test_client.get("/empty")

    assert response.text == "I am get method"

def test_get_method_with_query_params(app):
    bp = Blueprint("test_text_query_params")

    class DummyView(HTTPMethodView, attach=bp, uri="/query"):
        def get(self, request):
            return text("I am get method with query")

    app.blueprint(bp)
    request, response = app.test_client.get("/query?param=value")

    assert response.text == "I am get method with query"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")

    assert response.status == 404

def test_get_method_with_headers(app):
    bp = Blueprint("test_text_headers")

    class DummyView(HTTPMethodView, attach=bp, uri="/headers"):
        def get(self, request):
            return text("I am get method with headers")

    app.blueprint(bp)
    request, response = app.test_client.get("/headers", headers={"Custom-Header": "value"})

    assert response.text == "I am get method with headers"