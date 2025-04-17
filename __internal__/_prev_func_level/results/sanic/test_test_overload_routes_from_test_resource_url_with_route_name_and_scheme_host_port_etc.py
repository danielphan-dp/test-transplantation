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
    request, response = app.test_client.get('/url-for')
    assert response.status == 200
    assert response.text == 'url-for'

def test_url_for_with_invalid_route(app):
    with pytest.raises(URLBuildError):
        app.url_for("non_existent_route")

def test_url_for_with_query_params(app):
    @app.route('/url-with-params')
    def url_with_params(request):
        return text('params received')

    request, response = app.test_client.get('/url-with-params?param1=value1&param2=value2')
    assert response.status == 200
    assert response.text == 'params received'

def test_url_for_with_different_methods(app):
    @app.route('/method-test', methods=["GET", "POST"])
    async def method_test(request):
        if request.method == "POST":
            return text('POST method')
        return text('GET method')

    request, response = app.test_client.get('/method-test')
    assert response.status == 200
    assert response.text == 'GET method'

    request, response = app.test_client.post('/method-test')
    assert response.status == 200
    assert response.text == 'POST method'

def test_url_for_with_route_name(app):
    @app.route('/named-route', name='named_route')
    def named_route(request):
        return text('named route')

    assert app.url_for('named_route') == '/named-route'
    request, response = app.test_client.get(app.url_for('named_route'))
    assert response.status == 200
    assert response.text == 'named route'