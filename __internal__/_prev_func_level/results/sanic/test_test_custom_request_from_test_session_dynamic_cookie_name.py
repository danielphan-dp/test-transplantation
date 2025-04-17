import json
from sanic import Sanic
from sanic.response import text

def test_get_method():
    app = Sanic(name="Test")

    @app.route("/get")
    async def get_handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")

    assert request.body == b""
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_invalid_route():
    app = Sanic(name="Test")

    request, response = app.test_client.get("/invalid_route")

    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_custom_headers():
    app = Sanic(name="Test")

    @app.route("/get")
    async def get_handler(request):
        return text("I am get method")

    headers = {"Custom-Header": "CustomValue"}
    request, response = app.test_client.get("/get", headers=headers)

    assert request.headers.get("Custom-Header") == "CustomValue"
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_query_parameters():
    app = Sanic(name="Test")

    @app.route("/get")
    async def get_handler(request):
        return text(f"Query param: {request.args.get('param')}")

    request, response = app.test_client.get("/get?param=test")

    assert request.body == b""
    assert response.text == "Query param: test"
    assert response.status == 200