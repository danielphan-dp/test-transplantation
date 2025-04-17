import pytest
from sanic import Sanic, Request, response

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_head_method_not_allowed(app):
    @app.get("/")
    async def test_get(request: Request):
        return response.json({"hello": "world"})

    request, response = app.test_client.head("/")
    assert response.status == 200
    assert response.headers["Content-Length"] == "0"
    assert set(response.headers["Allow"].split(", ")) == {"GET"}

    app.router.reset()

    @app.post("/")
    async def test_post(request: Request):
        return response.json({"hello": "world"})

    request, response = app.test_client.head("/")
    assert response.status == 405
    assert set(response.headers["Allow"].split(", ")) == {"GET", "POST"}
    assert response.headers["Content-Length"] == "0"

    request, response = app.test_client.put("/")
    assert response.status == 405
    assert set(response.headers["Allow"].split(", ")) == {"GET", "POST"}
    assert response.headers["Content-Length"] == "0"

    request, response = app.test_client.delete("/")
    assert response.status == 405
    assert set(response.headers["Allow"].split(", ")) == {"GET", "POST"}
    assert response.headers["Content-Length"] == "0"