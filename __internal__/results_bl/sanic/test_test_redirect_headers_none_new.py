import pytest
from sanic.response import text

@pytest.fixture
def app():
    from sanic import Sanic
    app = Sanic("TestApp")

    @app.route("/get_method", methods=["GET"])
    def get_method(request):
        return text('I am get method')

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/get_method")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get_method?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'