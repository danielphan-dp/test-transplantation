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
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_ssl(app):
    @app.get("/ssl_test")
    async def handler(request):
        return text("ssl test")

    invalid_ssl = "invalid_cert_path"
    ssl_list = [invalid_ssl]

    with pytest.raises(ValueError) as excinfo:
        app.test_client.get("/ssl_test", server_kwargs={"ssl": ssl_list})

    assert "not found" in str(excinfo.value)
    assert invalid_ssl + "/fullchain.pem" in str(excinfo.value)