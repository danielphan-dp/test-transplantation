import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.put("/put_test")
    async def put_method(request):
        return text('I am put method')

    return app

def test_put_method(app):
    request, response = app.test_client.put("/put_test")
    assert response.text == "I am put method"

def test_put_method_with_data(app):
    request, response = app.test_client.put("/put_test", json={"key": "value"})
    assert response.text == "I am put method"

def test_put_method_invalid_route(app):
    request, response = app.test_client.put("/invalid_route")
    assert response.status == 404

def test_put_method_with_headers(app):
    request, response = app.test_client.put("/put_test", headers={"Custom-Header": "value"})
    assert response.text == "I am put method"