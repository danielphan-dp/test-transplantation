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
    def url_for(request):
        return text('url-for')

    new_kwargs = {
        "added_value_one": "one",
        "added_value_two": "two",
        "added_value_three": "three"
    }

    url = app.url_for("url_for", **new_kwargs)

    query = dict(parse_qsl(urlsplit(url).query))

    assert query["added_value_one"] == "one"
    assert query["added_value_two"] == "two"
    assert query["added_value_three"] == "three"

def test_url_for_with_no_query_params(app):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    url = app.url_for("url_for")

    query = dict(parse_qsl(urlsplit(url).query))

    assert query == {}

def test_url_for_fails_if_endpoint_not_found(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("non_existent_endpoint")
        assert e.match("Endpoint with name `app.non_existent_endpoint` was not found")