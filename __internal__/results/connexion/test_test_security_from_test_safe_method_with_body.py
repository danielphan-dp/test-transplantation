import pytest

def test_get_method_with_kwargs(secure_endpoint_app):
    app_client = secure_endpoint_app.test_client()

    # Test with no kwargs
    response_no_kwargs = app_client.get("/v1.0/get")
    assert response_no_kwargs.status_code == 200
    assert response_no_kwargs.json() == [{'name': 'get'}]

    # Test with single kwarg
    response_single_kwarg = app_client.get("/v1.0/get?arg1=value1")
    assert response_single_kwarg.status_code == 200
    assert response_single_kwarg.json() == {'name': 'get', 'arg1': 'value1'}

    # Test with multiple kwargs
    response_multiple_kwargs = app_client.get("/v1.0/get?arg1=value1&arg2=value2")
    assert response_multiple_kwargs.status_code == 200
    assert response_multiple_kwargs.json() == {'name': 'get', 'arg1': 'value1', 'arg2': 'value2'}

    # Test with empty kwargs
    response_empty_kwargs = app_client.get("/v1.0/get?")
    assert response_empty_kwargs.status_code == 200
    assert response_empty_kwargs.json() == [{'name': 'get'}]