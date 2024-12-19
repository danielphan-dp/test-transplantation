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
    def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_with_remote_addr(app, monkeypatch):
    access = Mock()
    monkeypatch.setattr(sanic.http.http1, "access_logger", access)

    @app.route("/get")
    def get_handler(request):
        return text('I am get method')

    headers = {"X-Forwarded-For": "1.1.1.1, 2.2.2.2"}
    request, response = app.test_client.get("/get", headers=headers)

    assert request.remote_addr == "1.1.1.1"
    access.info.assert_called_with(
        "",
        extra={
            "status": 200,
            "byte": len(response.content),
            "host": f"{request.remote_addr}:{request.port}",
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
    def get_handler(request):
        return text(f'I am get method with query param: {request.args.get("param", "none")}')

    request, response = app.test_client.get("/get?param=test")
    
    assert response.text == 'I am get method with query param: test'
    assert response.status == 200

def test_get_method_with_empty_query_params(app):
    @app.route("/get")
    def get_handler(request):
        return text(f'I am get method with query param: {request.args.get("param", "none")}')

    request, response = app.test_client.get("/get?param=")
    
    assert response.text == 'I am get method with query param: none'
    assert response.status == 200