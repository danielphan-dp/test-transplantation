import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def get_method(request: Request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_allowed(app):
    request, response = app.test_client.post("/")
    assert response.status == 405
    assert set(response.headers["Allow"].split(", ")) == {"GET"}

    request, response = app.test_client.put("/")
    assert response.status == 405
    assert set(response.headers["Allow"].split(", ")) == {"GET"}

    request, response = app.test_client.delete("/")
    assert response.status == 405
    assert set(response.headers["Allow"].split(", ")) == {"GET"}

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'  # Assuming the method does not change based on params

def test_get_method_content_type(app):
    request, response = app.test_client.get("/")
    assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'