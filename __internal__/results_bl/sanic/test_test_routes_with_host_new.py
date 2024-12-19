import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')
    return app

def test_url_for(app):
    request = app.test_client.get('/url-for')
    assert request.status == 200
    assert request.text == 'url-for'

def test_url_for_with_invalid_route(app):
    request = app.test_client.get('/invalid-url')
    assert request.status == 404

def test_url_for_with_query_parameters(app):
    request = app.test_client.get('/url-for?param=value')
    assert request.status == 200
    assert request.text == 'url-for'

def test_url_for_with_external_url(app):
    assert app.url_for('url_for', _external=True) == 'http://localhost/url-for'