import json
import pytest
from connexion import FlaskApp

@pytest.fixture
def simple_openapi_app():
    app = FlaskApp(__name__)
    return app

def test_json_method_with_valid_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.get("/v1.0/exploded-deep-object-param?id[foo]=bar")
    assert response.status_code == 200, response.text
    response_data = response.json()
    assert response_data['foo'] == 'bar'

def test_json_method_with_empty_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.get("/v1.0/exploded-deep-object-param?id[foo]=")
    assert response.status_code == 200, response.text
    response_data = response.json()
    assert response_data['foo'] == ''

def test_json_method_with_invalid_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.get("/v1.0/exploded-deep-object-param?id[foo]=bar&id[fooint]=not_a_number")
    assert response.status_code == 200, response.text
    response_data = response.json()
    assert response_data['fooint'] == 'not_a_number'

def test_json_method_with_boolean_string(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.get("/v1.0/exploded-deep-object-param?id[fooboo]=true")
    assert response.status_code == 200, response.text
    response_data = response.json()
    assert response_data['fooboo'] is True

def test_json_method_with_missing_parameters(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.get("/v1.0/exploded-deep-object-param")
    assert response.status_code == 200, response.text
    response_data = response.json()
    assert 'foo' not in response_data
    assert 'fooint' not in response_data
    assert 'fooboo' not in response_data