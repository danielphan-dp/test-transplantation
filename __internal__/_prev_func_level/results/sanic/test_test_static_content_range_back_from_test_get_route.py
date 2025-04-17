import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('path', ['/'])
def test_get_method(app, path):
    request, response = app.test_client.get(path)
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_path(app):
    request, response = app.test_client.get('/invalid')
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app):
    headers = {"Custom-Header": "TestValue"}
    request, response = app.test_client.get('/', headers=headers)
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers.get("Custom-Header") is None

def test_get_method_with_query_params(app):
    request, response = app.test_client.get('/?param=value')
    assert response.status == 200
    assert response.text == 'I am get method'