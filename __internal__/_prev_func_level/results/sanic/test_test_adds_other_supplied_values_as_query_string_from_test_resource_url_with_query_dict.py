import pytest
from urllib.parse import parse_qsl, urlsplit
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_with_additional_query_params(app):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    new_kwargs = {
        "param_one": "value_one",
        "param_two": "value_two",
        "param_three": "value_three"
    }

    url = app.url_for("url_for", **new_kwargs)

    query = dict(parse_qsl(urlsplit(url).query))

    assert query["param_one"] == "value_one"
    assert query["param_two"] == "value_two"
    assert query["param_three"] == "value_three"

def test_url_for_with_missing_params(app):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    with pytest.raises(URLBuildError) as e:
        app.url_for("url_for", missing_param="value")
        assert e.match("Required parameter `missing_param` was not passed to url_for")

def test_url_for_with_empty_params(app):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    url = app.url_for("url_for", empty_param="")
    query = dict(parse_qsl(urlsplit(url).query))

    assert "empty_param" in query
    assert query["empty_param"] == ""