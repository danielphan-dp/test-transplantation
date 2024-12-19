import string
from urllib.parse import parse_qsl, urlsplit
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.route('/url-for')
def url_for(request):
    return text('url-for')

def test_url_for_returns_correct_text(app):
    request = app.test_request_context('/url-for')
    response = url_for(request)
    assert response.body.decode() == 'url-for'

def test_url_for_with_query_string(app):
    @app.route('/url-for')
    def url_for_with_query(request):
        return text('url-for with query')

    new_kwargs = {"param_one": "value_one", "param_two": "value_two"}
    url = app.url_for("url_for_with_query", **new_kwargs)

    query = dict(parse_qsl(urlsplit(url).query))

    assert query["param_one"] == "value_one"
    assert query["param_two"] == "value_two"

def test_url_for_with_no_query_string(app):
    url = app.url_for("url_for")
    assert url == '/url-for'  # Ensure it returns the correct URL without query parameters

def test_url_for_invalid_route(app):
    with pytest.raises(Exception):
        app.url_for("non_existent_route")  # Test for URLBuildError when route does not exist