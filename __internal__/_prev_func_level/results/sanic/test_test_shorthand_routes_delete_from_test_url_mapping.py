import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_delete_method(app):
    @app.delete("/delete")
    def handler(request):
        return text("I am delete method")

    request, response = app.test_client.delete("/delete")
    assert response.text == "I am delete method"

    request, response = app.test_client.get("/delete")
    assert response.status == 405

    request, response = app.test_client.post("/delete")
    assert response.status == 405

    request, response = app.test_client.put("/delete")
    assert response.status == 405

    request, response = app.test_client.patch("/delete")
    assert response.status == 405

    request, response = app.test_client.options("/delete")
    assert response.status == 405

    request, response = app.test_client.head("/delete")
    assert response.status == 405