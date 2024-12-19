import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test")
    return app

@app.get("/get")
def get_handler(request):
    return text('I am get method')

def test_get_method(app):
    _, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    _, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_custom_header(app):
    @app.get("/get_with_header")
    def handler(request):
        return text('Header received', headers={'X-Custom-Header': 'value'})

    _, response = app.test_client.get("/get_with_header", headers={'X-Custom-Header': 'value'})
    assert response.status == 200
    assert response.text == 'Header received'