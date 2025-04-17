import pytest

def test_get_method_with_kwargs(secure_api_app):
    app_client = secure_api_app.test_client()
    
    # Test with valid kwargs
    response = app_client.get("/v1.0/get", query_string={"key": "value"})
    assert response.status_code == 200
    assert response.json == {'key': 'value', 'name': 'get'}

    # Test with multiple kwargs
    response = app_client.get("/v1.0/get", query_string={"key1": "value1", "key2": "value2"})
    assert response.status_code == 200
    assert response.json == {'key1': 'value1', 'key2': 'value2', 'name': 'get'}

    # Test with no kwargs
    response = app_client.get("/v1.0/get")
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]

    # Test with invalid endpoint
    response = app_client.get("/v1.0/invalid-endpoint")
    assert response.status_code == 404
    assert response.headers.get("content-type") == "application/problem+json"