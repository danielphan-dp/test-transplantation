import pytest
from sanic import Sanic
from sanic.text import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def handler(request):
        return text('I am get method')

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.status_code == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status_code == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.status_code == 200
    assert response.text == "I am get method"  # Assuming the handler does not change based on params

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.status_code == 200
    assert response.text == "I am get method"  # Assuming the handler does not change based on headers

def test_get_method_with_empty_request(app):
    request, response = app.test_client.get("/get", data={})
    assert response.status_code == 200
    assert response.text == "I am get method"  # Assuming the handler does not change with empty data