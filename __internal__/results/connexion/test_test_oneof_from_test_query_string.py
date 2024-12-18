import pytest
from connexion import FlaskApp

@pytest.fixture
def simple_openapi_app():
    app = FlaskApp(__name__)
    return app

def test_get_with_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    
    response = app_client.get("/v1.0/get", query_string={"key1": "value1", "key2": "value2"})
    assert response.status_code == 200
    assert response.json == {'key1': 'value1', 'key2': 'value2', 'name': 'get'}

def test_get_without_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    
    response = app_client.get("/v1.0/get")
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]

def test_get_with_empty_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    
    response = app_client.get("/v1.0/get", query_string={})
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]

def test_get_with_numeric_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    
    response = app_client.get("/v1.0/get", query_string={"number": 123})
    assert response.status_code == 200
    assert response.json == {'number': 123, 'name': 'get'}

def test_get_with_boolean_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    
    response = app_client.get("/v1.0/get", query_string={"flag": True})
    assert response.status_code == 200
    assert response.json == {'flag': True, 'name': 'get'}