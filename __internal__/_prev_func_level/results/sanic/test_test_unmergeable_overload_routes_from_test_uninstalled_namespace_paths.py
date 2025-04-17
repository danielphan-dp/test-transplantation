import os
import pytest
from sanic import Sanic
from sanic.response import text
from sanic_routing.exceptions import RouteExists

@pytest.fixture(autouse=True)
def reset():
    try:
        del os.environ['SANIC_MOTD_OUTPUT']
    except KeyError:
        pass

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_route_reset_after_deletion(app):
    @app.route("/test_route", methods=["GET"])
    async def test_handler(request):
        return text("Test OK")

    request, response = app.test_client.get("/test_route")
    assert response.text == "Test OK"

    app.router.reset()

    with pytest.raises(RouteExists):
        @app.route("/test_route", methods=["POST"])
        async def duplicate_handler(request):
            return text("Duplicate OK")

    request, response = app.test_client.post("/test_route")
    assert response.status == 405

def test_environment_variable_reset(app):
    os.environ['SANIC_MOTD_OUTPUT'] = 'Some Value'
    reset()
    assert 'SANIC_MOTD_OUTPUT' not in os.environ

def test_multiple_methods_on_same_route(app):
    @app.route("/multi_method", methods=["GET", "POST"])
    async def multi_handler(request):
        return text("Multi OK")

    request, response = app.test_client.get("/multi_method")
    assert response.text == "Multi OK"

    request, response = app.test_client.post("/multi_method")
    assert response.text == "Multi OK"

    app.router.reset()

    @app.route("/multi_method", methods=["PUT"])
    async def multi_put_handler(request):
        return text("Multi PUT OK")

    request, response = app.test_client.put("/multi_method")
    assert response.text == "Multi PUT OK"