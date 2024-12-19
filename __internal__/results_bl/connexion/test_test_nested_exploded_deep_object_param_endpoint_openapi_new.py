import json
import pytest
from connexion import FlaskApp

@pytest.fixture
def simple_openapi_app():
    app = FlaskApp(__name__)
    return app

def test_json_method_with_valid_text(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    simple_openapi_app.text = '{"key": "value"}'
    result = simple_openapi_app.json()
    assert result == {"key": "value"}

def test_json_method_with_empty_text(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    simple_openapi_app.text = ''
    with pytest.raises(json.JSONDecodeError):
        simple_openapi_app.json()

def test_json_method_with_invalid_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    simple_openapi_app.text = '{key: value}'  # Invalid JSON
    with pytest.raises(json.JSONDecodeError):
        simple_openapi_app.json()

def test_json_method_with_nested_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    simple_openapi_app.text = '{"foo": {"bar": "baz"}}'
    result = simple_openapi_app.json()
    assert result == {"foo": {"bar": "baz"}} 

def test_json_method_with_large_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    large_data = '{"' + '": "value", "'.join(f"key{i}" for i in range(1000)) + '": "value"}'
    simple_openapi_app.text = large_data
    result = simple_openapi_app.json()
    assert len(result) == 1000