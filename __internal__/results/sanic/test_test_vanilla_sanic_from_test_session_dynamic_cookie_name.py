import pytest
from sanic import Sanic, Blueprint, text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.route("/")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    @app.route("/not_found")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/non_existent")
    assert response.status == 404

def test_get_method_with_query_param(app):
    @app.route("/query")
    def get_method(request):
        return text(f"Query param received: {request.args.get('param', 'None')}")

    request, response = app.test_client.get("/query?param=test")
    assert response.text == "Query param received: test"

def test_get_method_with_empty_query_param(app):
    @app.route("/query")
    def get_method(request):
        return text(f"Query param received: {request.args.get('param', 'None')}")

    request, response = app.test_client.get("/query?param=")
    assert response.text == "Query param received: "