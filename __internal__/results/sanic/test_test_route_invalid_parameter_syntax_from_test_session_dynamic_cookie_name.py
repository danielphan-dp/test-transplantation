import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import InvalidUsage

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def get(request):
        return text('I am get method')

    return app

def test_get_method_valid_request(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    with pytest.raises(InvalidUsage):
        request, response = app.test_client.get("/get/<:str>")  # Invalid route syntax

def test_get_method_no_parameters(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"