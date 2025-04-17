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
        return text('I am delete method')

    request, response = app.test_client.delete("/delete")
    assert response.text == 'I am delete method'

    request, response = app.test_client.get("/delete")
    assert response.status == 405

def test_delete_method_not_found(app):
    request, response = app.test_client.delete("/nonexistent")
    assert response.status == 404

def test_delete_method_with_invalid_method(app):
    request, response = app.test_client.post("/delete")
    assert response.status == 405

def test_delete_method_with_query_params(app):
    @app.delete("/delete")
    def handler(request):
        return text('I am delete method with query')

    request, response = app.test_client.delete("/delete?param=value")
    assert response.text == 'I am delete method with query'