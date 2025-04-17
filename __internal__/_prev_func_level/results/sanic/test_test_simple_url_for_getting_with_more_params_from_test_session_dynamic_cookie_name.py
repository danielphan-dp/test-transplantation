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

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_empty_response(app):
    @app.route("/empty")
    def empty_response(request):
        return text("")

    request, response = app.test_client.get("/empty")
    assert response.status == 200
    assert response.text == ""