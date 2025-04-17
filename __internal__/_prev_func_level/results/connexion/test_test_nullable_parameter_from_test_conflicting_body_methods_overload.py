import pytest

def test_put_method(simple_app):
    app_client = simple_app.test_client()
    
    # Test with no arguments
    kwargs = {}
    resp = app_client.put("/v1.0/nullable-parameters", json=kwargs)
    assert resp.status_code == 201
    assert resp.json() == {'name': 'put'}

    # Test with additional parameters
    kwargs = {'param1': 'value1', 'param2': 'value2'}
    resp = app_client.put("/v1.0/nullable-parameters", json=kwargs)
    assert resp.status_code == 201
    assert resp.json() == {'name': 'put', 'param1': 'value1', 'param2': 'value2'}

    # Test with empty parameters
    kwargs = {}
    resp = app_client.put("/v1.0/nullable-parameters", json=kwargs)
    assert resp.status_code == 201
    assert resp.json() == {'name': 'put'}

    # Test with invalid content type
    headers = {"Content-Type": "text/plain"}
    resp = app_client.put("/v1.0/nullable-parameters", data="Invalid data", headers=headers)
    assert resp.status_code == 415  # Unsupported Media Type

    # Test with null values
    kwargs = {'param1': None}
    resp = app_client.put("/v1.0/nullable-parameters", json=kwargs)
    assert resp.status_code == 201
    assert resp.json() == {'name': 'put', 'param1': None}