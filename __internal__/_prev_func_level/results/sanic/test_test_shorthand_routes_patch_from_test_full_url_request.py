import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.patch("/patch")
    def handler(request):
        return text("I am patch method")

    return app

def test_patch_method_success(app):
    request, response = app.test_client.patch("/patch")
    assert response.text == "I am patch method"
    assert response.status == 200

def test_patch_method_invalid_method(app):
    request, response = app.test_client.get("/patch")
    assert response.status == 405

def test_patch_method_with_data(app):
    request, response = app.test_client.patch("/patch", data={"key": "value"})
    assert response.text == "I am patch method"
    assert response.status == 200

def test_patch_method_with_empty_data(app):
    request, response = app.test_client.patch("/patch", data={})
    assert response.text == "I am patch method"
    assert response.status == 200

def test_patch_method_not_found(app):
    request, response = app.test_client.patch("/nonexistent")
    assert response.status == 404