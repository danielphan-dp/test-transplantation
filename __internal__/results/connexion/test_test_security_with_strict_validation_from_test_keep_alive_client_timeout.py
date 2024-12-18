import pytest

@pytest.mark.parametrize("kwargs, expected", [
    ({"key1": "value1"}, {"name": "get", "key1": "value1"}),
    ({"key2": "value2", "key3": "value3"}, {"name": "get", "key2": "value2", "key3": "value3"}),
    ({}, [{"name": "get"}]),
])
def test_get_method_with_kwargs(secure_endpoint_strict_app, kwargs, expected):
    app_client = secure_endpoint_strict_app.test_client()
    
    res = app_client.get("/v1.0/test_apikey_query_parameter_validation", params=kwargs)
    
    if kwargs:
        assert res.status_code == 200
        assert res.json() == expected
    else:
        assert res.status_code == 200
        assert res.json() == expected