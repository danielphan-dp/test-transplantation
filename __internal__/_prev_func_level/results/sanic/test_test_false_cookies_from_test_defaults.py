import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

@pytest.mark.parametrize('request_method, expected_response', [
    ('GET', 'I am get method'),
    ('POST', 'Method POST not allowed for URL /'),
])
def test_get_method(app, request_method, expected_response):
    @app.route("/", methods=["GET", "POST"])
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.request(request_method, "/")
    
    if request_method == 'GET':
        assert response.text == expected_response
    else:
        assert response.status == 405
        assert "Method POST not allowed for URL /" in response.text

def test_get_method_no_route(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_custom_header(app):
    @app.route("/")
    def handler(request):
        return text('I am get method', headers={'X-Custom-Header': 'value'})

    request, response = app.test_client.get("/")
    assert response.headers['X-Custom-Header'] == 'value'