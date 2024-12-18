import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_with_no_params(app):
    @app.route("/no_params")
    def no_params(request):
        return text("no params")

    url = app.url_for("no_params")
    assert url == "/no_params"
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == "no params"

def test_url_for_with_extra_params(app):
    @app.route("/extra_params/<param>")
    def extra_params(request, param):
        return text(f"param: {param}")

    url = app.url_for("extra_params", param="test")
    assert url == "/extra_params/test"
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == "param: test"

def test_fails_url_build_if_param_not_passed(app):
    @app.route("/param_required/<param>")
    def param_required(request, param):
        return text(f"param: {param}")

    with pytest.raises(URLBuildError) as e:
        app.url_for("param_required")
        assert e.match("Required parameter `param` was not passed to url_for")

def test_fails_url_build_if_invalid_endpoint(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("invalid_endpoint")
        assert e.match("Endpoint with name `invalid_endpoint` was not found")