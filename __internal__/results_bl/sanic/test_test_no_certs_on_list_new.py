import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_response(app):
    @app.get("/get")
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_no_ssl(app):
    @app.get("/get_no_ssl")
    async def handler(request):
        return text('I am get method without SSL')

    ssl_list = [None]
    with pytest.raises(ValueError) as excinfo:
        app.test_client.get("/get_no_ssl", server_kwargs={"ssl": ssl_list})

    assert "No certificates" in str(excinfo.value)

def test_get_method_with_ssl(app):
    @app.get("/get_with_ssl")
    async def handler(request):
        return text('I am get method with SSL')

    ssl_list = ["valid_cert.pem"]
    request, response = app.test_client.get("/get_with_ssl", server_kwargs={"ssl": ssl_list})
    assert response.status == 200
    assert response.text == 'I am get method with SSL'