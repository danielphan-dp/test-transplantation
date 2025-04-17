import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_get_method_response(app):
    request, response = app.test_client.get("/")
    
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/?param=value")
    
    assert response.status == 200
    assert response.text == "I am get method"  # Assuming the method does not change based on query params

def test_get_method_with_headers(app):
    headers = {"Custom-Header": "value"}
    request, response = app.test_client.get("/", headers=headers)
    
    assert response.status == 200
    assert response.text == "I am get method"  # Assuming the method does not change based on headers

def test_get_method_with_invalid_method(app):
    request, response = app.test_client.post("/")
    
    assert response.status == 405
    assert "Method POST not allowed for URL /" in response.text