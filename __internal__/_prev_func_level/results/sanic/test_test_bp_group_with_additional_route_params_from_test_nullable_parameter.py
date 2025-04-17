import pytest
from sanic import Sanic
from sanic.response import text
from sanic.request import Request
from sanic.blueprints import Blueprint

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_put_method(app):
    @app.put("/put_test")
    async def put_method(request: Request):
        return text("I am put method")

    _, response = app.test_client.put("/put_test")
    assert response.text == "I am put method"

def test_put_method_with_auth(app):
    AUTH = "secret"
    header = {"authorization": "Basic " + AUTH}

    @app.put("/put_auth_test")
    async def put_auth_method(request: Request):
        auth = request.headers.get("authorization")
        if auth == "Basic " + AUTH:
            return text("Authorized PUT")
        return text("Unauthorized", status=401)

    _, response = app.test_client.put("/put_auth_test", headers=header)
    assert response.text == "Authorized PUT"

    _, response = app.test_client.put("/put_auth_test")
    assert response.status == 401

def test_put_method_with_invalid_data(app):
    @app.put("/put_invalid_data")
    async def put_invalid_data(request: Request):
        if not request.body:
            return text("No data provided", status=400)
        return text("Data received")

    _, response = app.test_client.put("/put_invalid_data")
    assert response.status == 400
    assert response.text == "No data provided"

def test_put_method_with_streaming(app):
    @app.put("/put_stream")
    async def put_stream(request: Request):
        result = ""
        while True:
            body = await request.stream.read()
            if body is None:
                break
            result += body.decode("utf-8")
        return text(result)

    data = "streaming data"
    _, response = app.test_client.put("/put_stream", data=data)
    assert response.text == data

def test_put_method_with_json(app):
    @app.put("/put_json")
    async def put_json(request: Request):
        return text(request.json)

    _, response = app.test_client.put("/put_json", json={"key": "value"})
    assert response.text == '{"key": "value"}'