import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test_get")
    def handler(request):
        return text("I am get method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/test_get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_unicode(app):
    request, response = app.test_client.get("/你好")
    assert response.status == 404  # Assuming this route is not defined

def test_get_method_with_param(app):
    @app.route("/overload/<param>", methods=["GET"], unquote=True)
    async def handler_with_param(request, param):
        return text("OK2 " + param)

    request, response = app.test_client.get("/overload/测试")
    assert response.status == 200
    assert response.text == "OK2 测试"