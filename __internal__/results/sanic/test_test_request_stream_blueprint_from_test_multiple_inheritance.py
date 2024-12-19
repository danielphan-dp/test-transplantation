import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_delete_method(app):
    @app.delete("/delete")
    async def delete(request):
        return text("I am delete method")

    request, response = app.test_client.delete("/delete")
    assert response.status == 200
    assert response.text == "I am delete method"

def test_delete_method_not_found(app):
    request, response = app.test_client.delete("/nonexistent")
    assert response.status == 404

def test_delete_method_with_query_params(app):
    @app.delete("/delete_with_params")
    async def delete_with_params(request):
        return text(f"Deleted item with id: {request.args.get('id')}")

    request, response = app.test_client.delete("/delete_with_params?id=123")
    assert response.status == 200
    assert response.text == "Deleted item with id: 123"

def test_delete_method_with_body(app):
    @app.delete("/delete_with_body")
    async def delete_with_body(request):
        return text(f"Body received: {request.body.decode('utf-8')}")

    request, response = app.test_client.delete("/delete_with_body", data="Sample body")
    assert response.status == 200
    assert response.text == "Body received: Sample body"