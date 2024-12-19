import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.get("/get")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_ssl(app):
    @app.get("/get_ssl")
    async def handler(request):
        return text("SSL test")

    ssl_dict = {"cert": "path/to/cert.pem", "key": "path/to/key.pem"}
    request, response = app.test_client.get("/get_ssl", server_kwargs={"ssl": ssl_dict})
    assert response.text == "SSL test"
    assert response.status == 200

def test_get_method_ssl_missing_cert(app):
    @app.get("/get_ssl_missing_cert")
    async def handler(request):
        return text("SSL test missing cert")

    ssl_dict = {"cert": None, "key": "path/to/key.pem"}
    with pytest.raises(ValueError) as excinfo:
        app.test_client.get("/get_ssl_missing_cert", server_kwargs={"ssl": ssl_dict})
    assert str(excinfo.value) == "SSL dict needs filenames for cert and key."

def test_get_method_ssl_missing_key(app):
    @app.get("/get_ssl_missing_key")
    async def handler(request):
        return text("SSL test missing key")

    ssl_dict = {"cert": "path/to/cert.pem", "key": None}
    with pytest.raises(ValueError) as excinfo:
        app.test_client.get("/get_ssl_missing_key", server_kwargs={"ssl": ssl_dict})
    assert str(excinfo.value) == "SSL dict needs filenames for cert and key."