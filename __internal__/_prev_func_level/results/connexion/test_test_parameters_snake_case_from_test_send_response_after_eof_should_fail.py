import pytest

def test_get_method_with_kwargs(snake_case_app):
    app_client = snake_case_app.test_client()
    response = app_client.get("/v1.0/test-get-path-snake/123?param1=value1&param2=value2")
    assert response.status_code == 200
    assert response.json() == {'name': 'get', 'param1': 'value1', 'param2': 'value2'}

def test_get_method_without_kwargs(snake_case_app):
    app_client = snake_case_app.test_client()
    response = app_client.get("/v1.0/test-get-path-snake/123")
    assert response.status_code == 200
    assert response.json() == [{'name': 'get'}]

def test_get_method_with_empty_kwargs(snake_case_app):
    app_client = snake_case_app.test_client()
    response = app_client.get("/v1.0/test-get-path-snake/123?empty_param=")
    assert response.status_code == 200
    assert response.json() == [{'name': 'get'}]

def test_get_method_with_invalid_kwargs(snake_case_app):
    app_client = snake_case_app.test_client()
    response = app_client.get("/v1.0/test-get-path-snake/123?param1=invalid")
    assert response.status_code == 200
    assert response.json() == {'name': 'get', 'param1': 'invalid'}