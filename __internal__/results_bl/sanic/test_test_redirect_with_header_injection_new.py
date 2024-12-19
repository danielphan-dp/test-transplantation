import pytest
from sanic.response import text

def test_get_method_response(redirect_app):
    """
    Test the response of the get method.
    """
    request, response = redirect_app.test_client.get("/get_method")
    
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(redirect_app):
    """
    Test the response of the get method with an invalid route.
    """
    request, response = redirect_app.test_client.get("/invalid_route")
    
    assert response.status == 404

def test_get_method_with_query_parameters(redirect_app):
    """
    Test the response of the get method with query parameters.
    """
    request, response = redirect_app.test_client.get("/get_method?param=test")
    
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_header_injection(redirect_app):
    """
    Test the get method response with header injection.
    """
    headers = {'test-header': 'test-value'}
    request, response = redirect_app.test_client.get("/get_method", headers=headers)
    
    assert response.status == 200
    assert "test-header" not in response.headers
    assert response.text == "I am get method"