import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')
    return app

def test_url_for_valid_endpoint(app):
    expected_url = '/url-for'
    assert expected_url == app.url_for('url_for')

def test_url_for_invalid_endpoint(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for('non_existent_endpoint')
        assert e.match("Endpoint with name `app.non_existent_endpoint` was not found")

def test_url_for_with_query_params(app):
    expected_url = '/url-for?param=value'
    assert expected_url == app.url_for('url_for', param='value')

def test_url_for_with_multiple_query_params(app):
    expected_url = '/url-for?param1=value1&param2=value2'
    assert expected_url == app.url_for('url_for', param1='value1', param2='value2')

def test_url_for_with_special_characters(app):
    expected_url = '/url-for?param=%20%23%3F%26%2B'
    assert expected_url == app.url_for('url_for', param=' /#?&+')