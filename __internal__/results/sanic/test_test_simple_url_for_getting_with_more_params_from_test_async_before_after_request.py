import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('args,url', [
    ({}, "/myurl"),
    ({"param1": "value1"}, "/myurl?param1=value1"),
    ({"param1": "value1", "param2": "value2"}, "/myurl?param1=value1&param2=value2"),
])
def test_get_method_with_params(app, args, url):
    @app.route("/myurl")
    def passes(request):
        return text("this should pass")

    assert url == app.url_for("passes", **args)
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == "this should pass"

def test_get_method_response(app):
    @app.route("/get")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_invalid_params(app):
    @app.route("/get_with_param/<param>")
    def get_with_param(request, param):
        return text(f"I received {param}")

    request, response = app.test_client.get("/get_with_param/123")
    assert response.status == 200
    assert response.text == "I received 123"