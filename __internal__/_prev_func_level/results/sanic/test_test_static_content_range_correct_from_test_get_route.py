import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('request_path', ['/'])
def test_get_method(app, request_path):
    request, response = app.test_client.get(request_path)
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get('/invalid_route')
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_custom_headers(app):
    headers = {'Custom-Header': 'CustomValue'}
    request, response = app.test_client.get('/', headers=headers)
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers['Custom-Header'] == 'CustomValue'  # Assuming headers are passed through

def test_get_method_with_query_parameters(app):
    request, response = app.test_client.get('/?param=value')
    assert response.status == 200
    assert response.text == 'I am get method'  # Assuming query parameters do not affect response

def test_get_method_with_empty_request(app):
    request, response = app.test_client.get('/')
    assert response.status == 200
    assert response.text == 'I am get method'  # Ensure it handles empty requests correctly