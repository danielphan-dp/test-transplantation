import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.delete("/delete")
    async def delete(request):
        return text('I am delete method')

    return app

def test_delete_method(app):
    request, response = app.test_client.delete("/delete")
    assert response.status == 200
    assert response.text == "I am delete method"

def test_delete_method_not_found(app):
    request, response = app.test_client.delete("/nonexistent")
    assert response.status == 404

def test_delete_method_with_query_params(app):
    request, response = app.test_client.delete("/delete?param=value")
    assert response.status == 200
    assert response.text == "I am delete method"