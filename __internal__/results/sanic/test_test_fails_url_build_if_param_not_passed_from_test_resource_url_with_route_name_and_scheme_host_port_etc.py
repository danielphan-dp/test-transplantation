import string
import pytest
from sanic import Sanic
from sanic.exceptions import URLBuildError
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_with_missing_param(app):
    url = "/"
    for letter in string.ascii_lowercase:
        url += f"<{letter}>/"
    
    @app.route(url)
    def fail(request):
        return text("this should fail")

    fail_args = list(string.ascii_lowercase)
    fail_args.pop()  # Remove the last letter to simulate missing parameter
    fail_kwargs = {fail_arg: fail_arg for fail_arg in fail_args}

    with pytest.raises(URLBuildError) as e:
        app.url_for("fail", **fail_kwargs)
        assert e.match("Required parameter `z` was not passed to url_for")

def test_url_for_with_extra_param(app):
    url = "/<a>/"
    
    @app.route(url)
    def handler(request, a):
        return text("this should pass")

    extra_kwargs = {'a': 'test', 'b': 'extra'}
    result = app.url_for("handler", **extra_kwargs)
    assert result == "/test/"

def test_url_for_with_no_params(app):
    @app.route("/no_params")
    def no_params(request):
        return text("no params")

    result = app.url_for("no_params")
    assert result == "/no_params"

def test_url_for_with_invalid_endpoint(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("non_existent_endpoint")
        assert e.match("Endpoint with name `app.non_existent_endpoint` was not found")