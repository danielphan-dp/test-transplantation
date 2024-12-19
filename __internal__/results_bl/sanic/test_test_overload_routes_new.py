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

def test_route_exists_error(app):
    app.router.reset()
    with pytest.raises(RouteExists):
        @app.route("/overload", methods=["PUT", "DELETE"])
        async def handler3(request):
            return text("Duplicated")

def test_env_variable_removal(app):
    os.environ['SANIC_MOTD_OUTPUT'] = 'Test'
    reset()
    assert 'SANIC_MOTD_OUTPUT' not in os.environ

def test_missing_env_variable(app):
    reset()
    assert 'SANIC_MOTD_OUTPUT' not in os.environ

def test_invalid_method_overload(app):
    request, response = app.test_client.patch("/overload")
    assert response.status == 405

def test_multiple_methods(app):
    @app.route("/overload", methods=["GET", "POST"])
    async def handler4(request):
        return text("OK3")

    request, response = app.test_client.get("/overload")
    assert response.text == "OK3"

    request, response = app.test_client.post("/overload")
    assert response.text == "OK3"