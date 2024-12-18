import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('path', ['/url-for', '/url-for/'])
def test_url_for_endpoint(app, path):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    request, response = app.test_client.get(path)
    assert response.status == 200
    assert response.text == 'url-for'

def test_url_for_not_found(app):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    _, response = app.test_client.get('/non-existent-url')
    assert response.status == 404

def test_url_for_with_query_params(app):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    request, response = app.test_client.get('/url-for?param=value')
    assert response.status == 200
    assert response.text == 'url-for'