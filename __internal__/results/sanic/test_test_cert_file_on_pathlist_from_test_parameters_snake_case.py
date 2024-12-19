import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get-test")
    async def handler(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get-test")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_query_params(app):
    @app.get("/get-test-with-params")
    async def handler(request):
        return text(f"Received param: {request.args.get('param')}")

    request, response = app.test_client.get("/get-test-with-params?param=test")
    assert response.status == 200
    assert response.text == "Received param: test"

def test_get_method_no_params(app):
    @app.get("/get-test-no-params")
    async def handler(request):
        return text("No params received")

    request, response = app.test_client.get("/get-test-no-params")
    assert response.status == 200
    assert response.text == "No params received"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid-route")
    assert response.status == 404
    assert "Requested URL /invalid-route not found" in response.text

def test_get_method_with_ssl(app):
    ssl_list = ["path/to/cert.pem"]

    with pytest.raises(ValueError) as excinfo:
        app.test_client.get("/get-test", server_kwargs={"ssl": ssl_list})

    assert "folder expected" in str(excinfo.value)
    assert "path/to/cert.pem" in str(excinfo.value)