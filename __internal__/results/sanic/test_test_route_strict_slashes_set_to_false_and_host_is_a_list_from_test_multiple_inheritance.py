import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing import SanicTestClient

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_delete_method(app):
    @app.delete("/delete")
    def delete_handler(request):
        return text("I am delete method")

    test_client = SanicTestClient(app)
    request, response = test_client.delete("/delete")
    assert response.text == "I am delete method"

def test_delete_method_with_invalid_route(app):
    @app.delete("/delete")
    def delete_handler(request):
        return text("I am delete method")

    test_client = SanicTestClient(app)
    request, response = test_client.delete("/nonexistent")
    assert response.status == 404

def test_delete_method_with_different_hosts(app):
    @app.delete("/delete", host=["127.0.0.1", "example.com"])
    def delete_handler(request):
        return text("I am delete method")

    test_client = SanicTestClient(app)
    request, response = test_client.delete("http://127.0.0.1/delete")
    assert response.text == "I am delete method"

    request, response = test_client.delete("http://example.com/delete")
    assert response.text == "I am delete method"