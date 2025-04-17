import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_with_valid_route(app):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    url = app.url_for('url_for')
    assert url == '/url-for', url
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'url-for'

def test_url_for_with_nonexistent_route(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for('nonexistent_route')
        assert e.match("Endpoint with name `app.nonexistent_route` was not found")

def test_url_for_with_query_parameters(app):
    @app.route('/url-with-query')
    def url_with_query(request):
        return text(f"Query param: {request.args.get('param')}")

    url = app.url_for('url_with_query', param='test')
    assert url == '/url-with-query?param=test', url
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'Query param: test'

def test_url_for_with_multiple_query_parameters(app):
    @app.route('/url-with-multiple-queries')
    def url_with_multiple_queries(request):
        return text(f"Param1: {request.args.get('param1')}, Param2: {request.args.get('param2')}")

    url = app.url_for('url_with_multiple_queries', param1='value1', param2='value2')
    assert url == '/url-with-multiple-queries?param1=value1&param2=value2', url
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'Param1: value1, Param2: value2'

def test_url_for_with_invalid_parameter_type(app):
    @app.route('/url-with-int/<int:some_int>')
    def url_with_int(request, some_int):
        return text(f"Integer: {some_int}")

    url = app.url_for('url_with_int', some_int='not_an_int')
    with pytest.raises(URLBuildError) as e:
        app.test_client.get(url)
        assert e.match("Required parameter `some_int` was not passed to url_for")