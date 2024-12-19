import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('request_path', ['/'])
def test_get_method(app, request_path):
    request, response = app.test_client.get(request_path)
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.parametrize('request_path', ['/nonexistent'])
def test_get_method_not_found(app, request_path):
    request, response = app.test_client.get(request_path)
    assert response.status == 404
    assert "Requested URL" in response.text

@pytest.mark.parametrize('request_path', ['/'])
def test_get_method_with_headers(app, request_path):
    headers = {'Custom-Header': 'TestValue'}
    request, response = app.test_client.get(request_path, headers=headers)
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers['Custom-Header'] == 'TestValue'  # Assuming the header is passed through

@pytest.mark.parametrize('request_path', ['/'])
def test_get_method_empty_body(app, request_path):
    request, response = app.test_client.get(request_path)
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.body == b'I am get method'  # Check the raw body content

@pytest.mark.parametrize('request_path', ['/'])
def test_get_method_with_query_params(app, request_path):
    request, response = app.test_client.get(request_path + '?param=value')
    assert response.status == 200
    assert response.text == 'I am get method'  # Assuming query params do not affect the response