import base64
import secrets
import pytest
from sanic import Sanic, Request, text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text('I am get method')

    return app

def test_get_method_valid_request(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_request(app):
    request, response = app.test_client.get("/get", headers={"Invalid-Header": "value"})
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_empty_request(app):
    request, response = app.test_client.get("/get", data="")
    assert response.status == 200
    assert response.text == 'I am get method'