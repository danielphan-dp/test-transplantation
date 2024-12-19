import pytest
from sanic import Sanic
from sanic.response import text

app = Sanic("TestApp")

@app.route('/url-for')
def url_for(request):
    return text('url-for')

@pytest.fixture
def blueprint_app():
    return app

def test_url_for_returns_correct_response(blueprint_app):
    request = blueprint_app.test_client.get('/url-for')
    assert request.status == 200
    assert request.text == 'url-for'

def test_url_for_with_invalid_route(blueprint_app):
    request = blueprint_app.test_client.get('/invalid-url')
    assert request.status == 404

def test_url_for_with_query_params(blueprint_app):
    request = blueprint_app.test_client.get('/url-for?param=value')
    assert request.status == 200
    assert request.text == 'url-for'  # Ensure the response remains the same

def test_url_for_with_empty_request(blueprint_app):
    request = blueprint_app.test_client.get('/url-for')
    assert request.status == 200
    assert request.text == 'url-for'  # Ensure the response remains the same

def test_url_for_multiple_requests(blueprint_app):
    for _ in range(10):
        request = blueprint_app.test_client.get('/url-for')
        assert request.status == 200
        assert request.text == 'url-for'  # Ensure consistent response across multiple requests