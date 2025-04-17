import pytest
from sanic import Sanic, response
from sanic.request import Request

@pytest.fixture
def app():
    return Sanic("test_app")

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

def test_head_with_no_route(app):
    request, response = app.test_client.head("/nonexistent")
    assert response.status == 404
    assert response.headers["Content-Length"] == "0"