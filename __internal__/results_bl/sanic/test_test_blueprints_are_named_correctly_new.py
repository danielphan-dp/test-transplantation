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

def test_url_for_returns_correct_response(app, sanic_testing):
    request, response = sanic_testing(app).get('/url-for')
    assert response.status == 200
    assert response.text == 'url-for'

def test_url_for_invalid_route(app, sanic_testing):
    request, response = sanic_testing(app).get('/invalid-url')
    assert response.status == 404

def test_url_for_with_query_parameters(app, sanic_testing):
    request, response = sanic_testing(app).get('/url-for?param=value')
    assert response.status == 200
    assert response.text == 'url-for'