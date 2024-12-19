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
    request, response = app.test_client.get('/url-for')
    assert response.status == 200
    assert response.text == 'url-for'

def test_url_for_invalid_route(app):
    request, response = app.test_client.get('/invalid-url')
    assert response.status == 404

def test_url_for_with_query_params(app):
    request, response = app.test_client.get('/url-for?param=value')
    assert response.status == 200
    assert response.text == 'url-for'