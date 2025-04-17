import asyncio
import pytest
from sanic import Sanic, Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    blueprint = Blueprint("test_blueprint")

    @blueprint.head("/head")
    def head_handler(request):
        return text("OK")

    app.blueprint(blueprint)
    return app

def test_head_method_success(app):
    request, response = app.test_client.head("/head")
    assert response.status == 200
    assert response.body == b''  # HEAD should return no body

def test_head_method_not_found(app):
    request, response = app.test_client.head("/nonexistent")
    assert response.status == 404

def test_head_method_with_invalid_method(app):
    request, response = app.test_client.get("/head")
    assert response.status == 405

def test_head_method_with_empty_request(app):
    request, response = app.test_client.head("/")
    assert response.status == 404  # Assuming no route for root

def test_head_method_with_custom_headers(app):
    request, response = app.test_client.head("/head", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.headers.get("Custom-Header") is None  # HEAD should not return custom headers

def test_head_method_multiple_requests(app):
    for _ in range(10):
        request, response = app.test_client.head("/head")
        assert response.status == 200
        assert response.body == b''  # Consistency check for multiple requests