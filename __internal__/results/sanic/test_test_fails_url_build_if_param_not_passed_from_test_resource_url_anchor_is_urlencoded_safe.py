import string
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_with_no_params(app):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    url = app.url_for('url_for')
    assert url == '/url-for'

def test_url_for_with_extra_params(app):
    @app.route('/url-for/<param>')
    def url_for_with_param(request, param):
        return text(f'url-for with param: {param}')

    url = app.url_for('url_for_with_param', param='test')
    assert url == '/url-for/test'

def test_fails_url_build_if_param_not_passed(app):
    url = "/"

    for letter in string.ascii_lowercase:
        url += f"<{letter}>/"

    @app.route(url)
    def fail(request):
        return text("this should fail")

    fail_args = list(string.ascii_lowercase)
    fail_args.pop()

    fail_kwargs = {fail_arg: fail_arg for fail_arg in fail_args}

    with pytest.raises(URLBuildError) as e:
        app.url_for("fail", **fail_kwargs)
        assert e.match("Required parameter `z` was not passed to url_for")

def test_fails_if_endpoint_not_found(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("non_existent_endpoint")
        assert e.match("Endpoint with name `app.non_existent_endpoint` was not found")