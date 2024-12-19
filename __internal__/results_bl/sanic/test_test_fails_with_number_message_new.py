import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

app = Sanic("TestApp")

@app.route('/url-for')
def url_for(request):
    return text('url-for')

def test_url_for_valid_request(app):
    request = app.test_client.get('/url-for')
    assert request.status == 200
    assert request.text == 'url-for'

def test_url_for_invalid_route(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("non_existent_route")
        e.match("No route found for endpoint 'non_existent_route'")

def test_url_for_with_invalid_param(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("url-for", some_param="invalid")
        e.match("No route found for endpoint 'url-for' with parameters")

def test_url_for_with_missing_param(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("url-for", missing_param=None)
        e.match("Missing required parameter 'missing_param'")