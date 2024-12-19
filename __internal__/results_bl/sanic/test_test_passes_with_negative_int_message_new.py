import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.route("/get-test")
    def get_method(request):
        return text('I am get method')

    return app

def test_get_method(app):
    url = app.url_for("get_method")
    request, response = app.test_client.get(url)
    assert response.text == "I am get method"

def test_get_method_with_query_params(app):
    url = app.url_for("get_method") + "?param=value"
    request, response = app.test_client.get(url)
    assert response.text == "I am get method"

def test_get_method_with_empty_path(app):
    url = app.url_for("get_method") + "/"
    request, response = app.test_client.get(url)
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    url = "/invalid-route"
    request, response = app.test_client.get(url)
    assert response.status == 404

def test_get_method_with_large_integer(app):
    url = app.url_for("get_method") + "?large_int=999999999999999999"
    request, response = app.test_client.get(url)
    assert response.text == "I am get method"