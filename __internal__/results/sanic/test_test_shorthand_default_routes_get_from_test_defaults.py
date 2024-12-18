import pytest
from sanic import Sanic
from sanic.response import text

def test_get_method_response():
    app = Sanic("test_app")

    @app.get("/get")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_route_name():
    app = Sanic("test_app")

    @app.get("/get")
    def handler(request):
        return text("I am get method")

    assert app.router.routes_all[("get",)].name == "app.handler"

def test_get_method_url_for():
    app = Sanic("test_app")

    @app.get("/get")
    def handler(request):
        return text("I am get method")

    assert app.url_for("handler") == "/get"

def test_get_method_invalid_route():
    app = Sanic("test_app")

    request, response = app.test_client.get("/invalid")
    
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params():
    app = Sanic("test_app")

    @app.get("/get")
    def handler(request):
        return text(f"Query param foo: {request.args.get('foo')}")

    request, response = app.test_client.get("/get?foo=bar")
    
    assert response.status == 200
    assert response.text == "Query param foo: bar"