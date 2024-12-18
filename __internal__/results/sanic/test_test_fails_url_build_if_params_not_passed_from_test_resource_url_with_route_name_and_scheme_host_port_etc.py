import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_with_valid_route(app):
    @app.route("/valid")
    def valid_route(request):
        return text("this should pass")

    url = app.url_for("valid_route")
    assert url == "/valid"
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == "this should pass"

def test_url_for_with_external_scheme(app):
    @app.route("/external")
    def external_route(request):
        return text("this should pass")

    app.config.update({"SERVER_NAME": "example.com"})
    url = app.url_for("external_route", _scheme="http", _external=True)
    assert url == "http://example.com/external"
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == "this should pass"

def test_fails_url_build_if_params_not_passed(app):
    @app.route("/params/<param>")
    def params_route(request, param):
        return text(f"param: {param}")

    with pytest.raises(URLBuildError) as e:
        app.url_for("params_route")
        assert e.match("Required parameter `param` was not passed to url_for")

def test_fails_url_build_if_invalid_route(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("non_existent_route")
        assert e.match("Endpoint with name `app.non_existent_route` was not found")

def test_url_for_with_multiple_params(app):
    @app.route("/multi/<param1>/<param2>")
    def multi_params_route(request, param1, param2):
        return text(f"param1: {param1}, param2: {param2}")

    url = app.url_for("multi_params_route", param1="value1", param2="value2")
    assert url == "/multi/value1/value2"
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == "param1: value1, param2: value2"