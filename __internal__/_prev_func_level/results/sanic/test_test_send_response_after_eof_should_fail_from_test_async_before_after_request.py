import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    async def get_method(request: Request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_param(app):
    @app.get("/get_with_param")
    async def get_with_param(request: Request):
        param = request.args.get('param', 'default')
        return text(f'Param is {param}')

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.text == "Param is test"
    assert response.status == 200

def test_get_method_without_query_param(app):
    request, response = app.test_client.get("/get_with_param")
    assert response.text == "Param is default"
    assert response.status == 200

def test_get_method_with_logging(app, caplog):
    @app.get("/get_with_logging")
    async def get_with_logging(request: Request):
        app.logger.info("Logging from get method")
        return text('I am get method with logging')

    with caplog.at_level("INFO"):
        request, response = app.test_client.get("/get_with_logging")
        assert response.text == "I am get method with logging"
        assert "Logging from get method" in caplog.text