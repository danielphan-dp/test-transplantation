import os
import pytest
from sanic import Sanic, Request, response

@pytest.fixture(autouse=True)
def reset():
    try:
        del os.environ['SANIC_MOTD_OUTPUT']
    except KeyError:
        pass

def test_method_not_allowed_with_delete():
    app = Sanic("app")

    @app.get("/")
    async def test_get(request: Request):
        return response.json({"hello": "world"})

    request, response = app.test_client.delete("/")
    assert response.status == 405
    assert set(response.headers["Allow"].split(", ")) == {
        "GET",
    }
    assert response.headers["Content-Length"] == "0"

def test_method_not_allowed_with_options():
    app = Sanic("app")

    @app.get("/")
    async def test_get(request: Request):
        return response.json({"hello": "world"})

    request, response = app.test_client.options("/")
    assert response.status == 200
    assert set(response.headers["Allow"].split(", ")) == {
        "GET",
    }

    app.router.reset()

    @app.post("/")
    async def test_post(request: Request):
        return response.json({"hello": "world"})

    request, response = app.test_client.options("/")
    assert response.status == 200
    assert set(response.headers["Allow"].split(", ")) == {
        "GET",
        "POST",
    }