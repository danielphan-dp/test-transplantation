import pytest
from sanic.response import text

def test_get_method_response(redirect_app):
    """
    Test the response of the get method to ensure it returns the expected text.
    """
    request, response = redirect_app.test_client.get("/get_method")
    
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"

def test_get_method_invalid_route(redirect_app):
    """
    Test the response of the get method for an invalid route.
    """
    request, response = redirect_app.test_client.get("/invalid_route")
    
    assert response.status == 404

def test_get_method_with_query_params(redirect_app):
    """
    Test the get method with query parameters to ensure it handles them correctly.
    """
    request, response = redirect_app.test_client.get("/get_method?param=value")
    
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"