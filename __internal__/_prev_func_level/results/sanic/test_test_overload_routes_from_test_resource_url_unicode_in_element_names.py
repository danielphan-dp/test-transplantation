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
    @app.route('/params/<param>')
    def params_handler(request, param):
        return text(f'param: {param}')

    request, response = app.test_client.get('/params/test')
    assert response.status == 200
    assert response.text == 'param: test'

def test_url_for_with_query_params(app):
    @app.route('/query')
    def query_handler(request):
        return text(f'query: {request.args.get("param")}')

    request, response = app.test_client.get('/query?param=test')
    assert response.status == 200
    assert response.text == 'query: test'

def test_url_for_with_invalid_method(app):
    @app.route('/method', methods=['POST'])
    def method_handler(request):
        return text('method post')

    request, response = app.test_client.get('/method')
    assert response.status == 405  # Method Not Allowed

def test_url_for_with_multiple_routes(app):
    @app.route('/multi', methods=['GET'])
    def multi_get(request):
        return text('multi get')

    @app.route('/multi', methods=['POST'])
    def multi_post(request):
        return text('multi post')

    request, response = app.test_client.get('/multi')
    assert response.status == 200
    assert response.text == 'multi get'

    request, response = app.test_client.post('/multi')
    assert response.status == 200
    assert response.text == 'multi post'