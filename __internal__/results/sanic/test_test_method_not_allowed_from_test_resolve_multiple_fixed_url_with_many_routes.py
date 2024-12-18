import pytest
from sanic import Sanic, Request, response

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_head_method_allowed(app):
    @app.get("/")
    async def test_get(request: Request):
        return response.json({"hello": "world"})

    request, response = app.test_client.head("/")
    assert response.status == 200
    assert response.headers["Content-Length"] == "0"
    assert set(response.headers["Allow"].split(", ")) == {"GET"}

def test_head_method_not_allowed(app):
    @app.post("/")
    async def test_post(request: Request):
        return response.json({"hello": "world"})

    request, response = app.test_client.head("/")
    assert response.status == 405
    assert set(response.headers["Allow"].split(", ")) == {"GET", "POST"}
    assert response.headers["Content-Length"] == "0"

def test_head_method_with_no_routes(app):
    request, response = app.test_client.head("/nonexistent")
    assert response.status == 404
    assert "Allow" not in response.headers

def test_head_method_with_empty_body(app):
    @app.get("/empty")
    async def test_empty(request: Request):
        return response.text("")

    request, response = app.test_client.head("/empty")
    assert response.status == 200
    assert response.headers["Content-Length"] == "0"