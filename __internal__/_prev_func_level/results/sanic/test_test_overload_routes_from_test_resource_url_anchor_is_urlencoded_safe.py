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

def test_url_for_endpoint(app):
    request, response = app.test_client.get('/url-for')
    assert response.status == 200
    assert response.text == 'url-for'

def test_url_for_invalid_endpoint(app):
    with pytest.raises(URLBuildError):
        app.url_for("non_existent_route")

def test_url_for_with_params(app):
    @app.route('/url-for/<param>')
    def url_for_param(request, param):
        return text(f'url-for with param: {param}')

    request, response = app.test_client.get('/url-for/test')
    assert response.status == 200
    assert response.text == 'url-for with param: test'

def test_url_for_with_query_params(app):
    @app.route('/url-for-query')
    def url_for_query(request):
        return text(f'url-for with query: {request.args}')

    request, response = app.test_client.get('/url-for-query?key=value')
    assert response.status == 200
    assert response.text == 'url-for with query: MultiDict([(\'key\', [\'value\'])])'