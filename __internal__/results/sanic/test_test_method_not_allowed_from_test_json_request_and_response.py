import pytest
from sanic import Sanic, response
from sanic.request import Request

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.patch("/")
    async def patch_method(request: Request):
        return response.text("I am patch method")

    return app

def test_patch_method_allowed(app):
    request, response = app.test_client.patch("/")
    assert response.status == 200
    assert response.text == "I am patch method"

def test_patch_method_not_allowed(app):
    app.router.reset()

    @app.get("/")
    async def test_get(request: Request):
        return response.json({"hello": "world"})

    request, response = app.test_client.head("/")
    assert response.status == 405
    assert set(response.headers["Allow"].split(", ")) == {
        "GET",
    }
    assert response.headers["Content-Length"] == "0"

    request, response = app.test_client.post("/")
    assert response.status == 405
    assert set(response.headers["Allow"].split(", ")) == {
        "GET",
    }
    assert response.headers["Content-Length"] == "0"

    request, response = app.test_client.patch("/")
    assert response.status == 405
    assert set(response.headers["Allow"].split(", ")) == {
        "GET",
    }
    assert response.headers["Content-Length"] == "0"