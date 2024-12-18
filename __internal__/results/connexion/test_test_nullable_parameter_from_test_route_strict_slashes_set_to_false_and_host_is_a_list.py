import pytest

def test_put_method(simple_app):
    app_client = simple_app.test_client()
    
    # Test with no arguments
    resp = app_client.put("/v1.0/nullable-parameters")
    assert resp.json() == {'name': 'put'}

    # Test with additional keyword arguments
    resp = app_client.put("/v1.0/nullable-parameters", data={"extra_param": "value"})
    assert resp.json() == {'name': 'put', 'extra_param': 'value'}

    # Test with different types of arguments
    resp = app_client.put("/v1.0/nullable-parameters", data={"int_param": 123})
    assert resp.json() == {'name': 'put', 'int_param': 123}

    resp = app_client.put("/v1.0/nullable-parameters", data={"float_param": 123.45})
    assert resp.json() == {'name': 'put', 'float_param': 123.45}

    resp = app_client.put("/v1.0/nullable-parameters", data={"bool_param": True})
    assert resp.json() == {'name': 'put', 'bool_param': True}

    # Test with empty data
    resp = app_client.put("/v1.0/nullable-parameters", data={})
    assert resp.json() == {'name': 'put'}