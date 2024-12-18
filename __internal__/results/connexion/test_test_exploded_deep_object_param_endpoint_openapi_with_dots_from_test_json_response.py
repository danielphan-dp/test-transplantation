import pytest

@pytest.fixture
def simple_openapi_app():
    from connexion import FlaskApp
    app = FlaskApp(__name__)
    return app

def test_get_with_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    
    response = app_client.get("/v1.0/get?param1=value1&param2=value2")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {'name': 'get', 'param1': 'value1', 'param2': 'value2'}

def test_get_without_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    
    response = app_client.get("/v1.0/get")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == [{'name': 'get'}]

def test_get_with_empty_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    
    response = app_client.get("/v1.0/get?empty_param=")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {'name': 'get', 'empty_param': ''}