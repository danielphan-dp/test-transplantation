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

def test_url_for_basic(app):
    url = app.url_for('url_for')
    assert url == '/url-for', url
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'url-for'

def test_url_for_with_nonexistent_endpoint(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for('nonexistent')
        assert e.match("Endpoint with name `app.nonexistent` was not found")

def test_url_for_with_query_params(app):
    @app.route('/query')
    def query_handler(request):
        return text(f"Query param: {request.args.get('param')}")

    url = app.url_for('query_handler', param='test')
    assert url == '/query?param=test', url
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'Query param: test'

def test_url_for_with_multiple_params(app):
    @app.route('/multi/<int:id>/<string:name>')
    def multi_handler(request, id, name):
        return text(f"ID: {id}, Name: {name}")

    url = app.url_for('multi_handler', id=1, name='test')
    assert url == '/multi/1/test', url
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'ID: 1, Name: test'

def test_url_for_with_negative_int_param(app):
    @app.route('/negative/<int:num>')
    def negative_handler(request, num):
        return text(f"Negative number: {num}")

    url = app.url_for('negative_handler', num=-5)
    assert url == '/negative/-5', url
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'Negative number: -5'