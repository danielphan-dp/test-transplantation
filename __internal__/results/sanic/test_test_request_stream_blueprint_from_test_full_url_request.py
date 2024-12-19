import pytest
from sanic import Sanic
from sanic.response import text
from sanic.blueprints import Blueprint

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_patch_method(app):
    @app.patch("/patch")
    async def patch(request):
        return text("I am patch method")

    request, response = app.test_client.patch("/patch")
    assert response.status == 200
    assert response.text == "I am patch method"

    request, response = app.test_client.patch("/patch", data="Test data")
    assert response.status == 200
    assert response.text == "I am patch method"

    request, response = app.test_client.patch("/patch", data={"key": "value"})
    assert response.status == 200
    assert response.text == "I am patch method"

    request, response = app.test_client.patch("/patch", data=None)
    assert response.status == 200
    assert response.text == "I am patch method"