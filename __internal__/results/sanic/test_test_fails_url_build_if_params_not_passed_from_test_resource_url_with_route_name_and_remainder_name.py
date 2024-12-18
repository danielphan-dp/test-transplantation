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
    url = app.url_for("external_route", _external=True, _scheme="http")
    assert url == "http://example.com/external"
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == "this should pass"

def test_fails_url_build_if_endpoint_not_found(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("non_existent_route")
        assert e.match("Endpoint with name `app.non_existent_route` was not found")

def test_fails_url_build_if_param_not_passed(app):
    @app.route("/param/<param>")
    def param_route(request, param):
        return text(f"param: {param}")

    with pytest.raises(URLBuildError) as e:
        app.url_for("param_route")
        assert e.match("Required parameter `param` was not passed to url_for")

def test_fails_url_build_if_invalid_scheme(app):
    @app.route("/invalid_scheme")
    def invalid_scheme_route(request):
        return text("this should pass")

    with pytest.raises(ValueError) as e:
        app.url_for("invalid_scheme_route", _scheme="ftp")
        assert e.match("Invalid scheme specified")