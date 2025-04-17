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
    client = app.test_client()
    
    request, response = client.put("/put")
    assert response.status == 200
    assert response.text == "I am put method"

def test_put_method_with_data(app):
    client = app.test_client()
    
    data = {"key": "value"}
    request, response = client.put("/put", json=data)
    assert response.status == 200
    assert response.text == "I am put method"

def test_put_method_invalid_route(app):
    client = app.test_client()
    
    with pytest.raises(URLBuildError):
        app.url_for("non_existent_route")

def test_route_name(app):
    assert app.router.routes_all[("put",)].name == "app.route_put"
    assert app.url_for("route_put") == "/put"