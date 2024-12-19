import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.route("/delete", methods=["DELETE"])
    async def delete_handler(request):
        return text('I am delete method')

    return app

def test_delete_method(app):
    request, response = app.test_client.delete("/delete")
    assert response.text == "I am delete method"
    assert response.status == 200

def test_delete_method_not_allowed(app):
    request, response = app.test_client.get("/delete")
    assert response.status == 405

    request, response = app.test_client.post("/delete")
    assert response.status == 405

    request, response = app.test_client.put("/delete")
    assert response.status == 405

    request, response = app.test_client.options("/delete")
    assert response.status == 405

def test_delete_method_with_invalid_route(app):
    request, response = app.test_client.delete("/nonexistent")
    assert response.status == 404