import pytest
from sanic import Sanic
from sanic.response import text

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

def test_url_for_with_query_params(app):
    @app.route('/url-with-query')
    def url_with_query(request):
        return text('query received')

    url = app.url_for('url_with_query', param1='value1', param2='value2')
    assert url == '/url-with-query?param1=value1&param2=value2', url
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'query received'

def test_url_for_with_nonexistent_endpoint(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for('nonexistent_endpoint')
        assert str(e.value) == "Endpoint with name `nonexistent_endpoint` was not found"

def test_url_for_with_invalid_param(app):
    @app.route('/url-with-int/<int:some_int>')
    def url_with_int(request, some_int):
        return text(f'Integer received: {some_int}')

    url = app.url_for('url_with_int', some_int='not_an_int')
    with pytest.raises(URLBuildError) as e:
        app.test_client.get(url)
        assert str(e.value) == "Required parameter `some_int` was not passed to url_for"