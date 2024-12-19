import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.patch("/patch")
    async def handler(request):
        return text("I am patch method")

    return app

def test_patch_method_success(app):
    request, response = app.test_client.patch("/patch")
    assert response.status == 200
    assert response.text == "I am patch method"

def test_patch_method_not_allowed(app):
    request, response = app.test_client.get("/patch")
    assert response.status == 405

def test_patch_method_with_data(app):
    request, response = app.test_client.patch("/patch", data="Some data")
    assert response.status == 200
    assert response.text == "I am patch method"

def test_patch_method_invalid_route(app):
    request, response = app.test_client.patch("/invalid")
    assert response.status == 404

def test_patch_method_options(app):
    request, response = app.test_client.options("/patch")
    assert response.status == 200
    assert "PATCH" in response.headers.get("Allow")