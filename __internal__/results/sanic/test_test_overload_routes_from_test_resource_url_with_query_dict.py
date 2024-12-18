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

def test_url_for_with_query_params(app):
    @app.route('/url-for-with-params')
    def url_for_with_params(request):
        return text('url-for-with-params')

    request, response = app.test_client.get('/url-for-with-params?param1=value1&param2=value2')
    assert response.status == 200
    assert response.text == 'url-for-with-params'

def test_url_for_with_different_methods(app):
    @app.route('/url-for-post', methods=["POST"])
    def url_for_post(request):
        return text('url-for-post')

    request, response = app.test_client.post('/url-for-post')
    assert response.status == 200
    assert response.text == 'url-for-post'