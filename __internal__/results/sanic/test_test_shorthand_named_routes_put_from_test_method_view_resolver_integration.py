import asyncio
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.put("/put", name="route_put")
    async def handler(request):
        return text("I am put method")

    return app

def test_put_method(app):
    request, response = app.test_client.put("/put")
    assert response.status == 200
    assert response.text == "I am put method"

def test_put_method_url(app):
    assert app.router.routes_all[("put",)].name == "app.route_put"
    assert app.url_for("route_put") == "/put"

def test_invalid_url_build(app):
    with pytest.raises(URLBuildError):
        app.url_for("non_existent_handler")

def test_put_method_with_data(app):
    data = {"key": "value"}
    request, response = app.test_client.put("/put", json=data)
    assert response.status == 200
    assert response.text == "I am put method"  # Adjust based on actual implementation if needed

def test_put_method_empty_body(app):
    request, response = app.test_client.put("/put", data="")
    assert response.status == 200
    assert response.text == "I am put method"  # Adjust based on actual implementation if needed