import pytest

@pytest.mark.parametrize("kwargs, expected", [
    ({'key1': 'value1'}, {'key1': 'value1', 'name': 'get'}),
    ({'key2': 'value2', 'key3': 'value3'}, {'key2': 'value2', 'key3': 'value3', 'name': 'get'}),
    ({}, [{'name': 'get'}])
])
def test_get_method_with_kwargs(simple_app, kwargs, expected):
    app_client = simple_app.test_client()
    url = "/v1.0/get"
    response = app_client.get(url, query_string=kwargs)
    
    assert response.status_code == 200
    assert response.json == expected

def test_get_method_no_kwargs(simple_app):
    app_client = simple_app.test_client()
    url = "/v1.0/get"
    response = app_client.get(url)
    
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]