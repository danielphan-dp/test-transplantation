import pytest

def test_get_method_with_kwargs(secure_endpoint_app):
    app_client = secure_endpoint_app.test_client()
    
    # Test with valid kwargs
    response = app_client.get("/v1.0/getmethod", query_string={'key1': 'value1', 'key2': 'value2'})
    assert response.status_code == 200
    assert response.json == {'key1': 'value1', 'key2': 'value2', 'name': 'get'}

    # Test with empty kwargs
    response = app_client.get("/v1.0/getmethod")
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]

    # Test with single kwarg
    response = app_client.get("/v1.0/getmethod", query_string={'key1': 'value1'})
    assert response.status_code == 200
    assert response.json == {'key1': 'value1', 'name': 'get'}

    # Test with unexpected kwarg
    response = app_client.get("/v1.0/getmethod", query_string={'unexpected_key': 'unexpected_value'})
    assert response.status_code == 200
    assert response.json == {'unexpected_key': 'unexpected_value', 'name': 'get'}