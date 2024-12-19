import pytest
from unittest.mock import Mock, ANY
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_get_method")
    return app

def test_get_method_response(app):
    @app.route("/get")
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_access_log(app, monkeypatch):
    access = Mock()
    monkeypatch.setattr(sanic.http.http1, "access_logger", access)

    @app.route("/get")
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")

    access.info.assert_called_with(
        "",
        extra={
            "status": 200,
            "byte": len(response.content),
            "host": f"{request.ip}:{request.port}",
            "request": f"GET {request.scheme}://{request.host}/get",
            "duration": ANY,
        },
    )

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    @app.route("/get")
    async def get_method(request):
        return text(f'Query param: {request.args.get("param", "None")}')

    request, response = app.test_client.get("/get?param=test")
    assert response.status == 200
    assert response.text == 'Query param: test'