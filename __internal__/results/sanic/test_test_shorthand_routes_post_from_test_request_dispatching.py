import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method(app):
    @app.post("/post")
    def handler(request):
        return text("I am post method")

    request, response = app.test_client.post("/post")
    assert response.text == "I am post method"

    request, response = app.test_client.get("/post")
    assert response.status == 405

    request, response = app.test_client.put("/post")
    assert response.status == 405

    request, response = app.test_client.delete("/post")
    assert response.status == 405

    request, response = app.test_client.options("/post")
    assert response.status == 200
    assert "POST" in response.headers.get("Allow")