import os
import pytest
from sanic import Sanic
from sanic.response import text
from sanic_routing.exceptions.RouteExists

@pytest.fixture(autouse=True)
def reset():
    try:
        del os.environ['SANIC_MOTD_OUTPUT']
    except KeyError:
        pass

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.route("/overload", methods=["GET"])
    async def handler1(request):
        return text("OK1")

    @app.route("/overload", methods=["POST", "PUT"])
    async def handler2(request):
        return text("OK2")

    return app

def test_get_overload(app):
    request, response = app.test_client.get("/overload")
    assert response.text == "OK1"

def test_post_overload(app):
    request, response = app.test_client.post("/overload")
    assert response.text == "OK2"

def test_put_overload(app):
    request, response = app.test_client.put("/overload")
    assert response.text == "OK2"

def test_delete_overload(app):
    request, response = app.test_client.delete("/overload")
    assert response.status == 405

def test_duplicate_route_registration(app):
    app.router.reset()
    with pytest.raises(RouteExists):
        @app.route("/overload", methods=["PUT", "DELETE"])
        async def handler3(request):
            return text("Duplicated")