import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_delete_method(app):
    @app.route("/delete", methods=["DELETE"])
    async def delete_handler(request):
        return text('I am delete method')

    request, response = app.test_client.delete("/delete")
    assert response.text == "I am delete method"
    assert response.status == 200

def test_delete_method_not_allowed(app):
    @app.route("/delete", methods=["GET"])
    async def delete_handler(request):
        return text('I am delete method')

    request, response = app.test_client.delete("/delete")
    assert response.status == 405

def test_delete_method_with_invalid_route(app):
    @app.route("/delete", methods=["POST"])
    async def delete_handler(request):
        return text('I am delete method')

    request, response = app.test_client.delete("/delete")
    assert response.status == 405

def test_delete_method_with_nonexistent_route(app):
    request, response = app.test_client.delete("/nonexistent")
    assert response.status == 404