import string
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
    def url_for_view(request):
        return text('url-for')

    new_kwargs = {
        "added_value_one": "one",
        "added_value_two": "two",
        "extra_param": "extra"
    }

    url = app.url_for("url_for_view", **new_kwargs)

    query = dict(parse_qsl(urlsplit(url).query))

    assert query["added_value_one"] == "one"
    assert query["added_value_two"] == "two"
    assert query["extra_param"] == "extra"

def test_url_for_with_missing_required_param(app):
    @app.route('/url-for')
    def url_for_view(request):
        return text('url-for')

    with pytest.raises(URLBuildError) as e:
        app.url_for("url_for_view", added_value_one="one")
        assert e.match("Required parameter `added_value_two` was not passed to url_for")

def test_url_for_with_invalid_view_name(app):
    @app.route('/url-for')
    def url_for_view(request):
        return text('url-for')

    with pytest.raises(URLBuildError) as e:
        app.url_for("non_existent_view")
        assert e.match("Endpoint with name `app.non_existent_view` was not found")