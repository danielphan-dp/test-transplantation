import json
import pytest

def test_json_method_with_valid_json(simple_app):
    app_client = simple_app.test_client()
    data = json.dumps({"key": "value", "number": 123, "boolean": True})
    response = app_client.post("/v1.0/forward", data=data, content_type='application/json')

    assert response.status_code == 200
    assert response.json() == json.loads(data)

def test_json_method_with_empty_json(simple_app):
    app_client = simple_app.test_client()
    data = json.dumps({})
    response = app_client.post("/v1.0/forward", data=data, content_type='application/json')

    assert response.status_code == 200
    assert response.json() == json.loads(data)

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    data = "{invalid_json}"
    response = app_client.post("/v1.0/forward", data=data, content_type='application/json')

    assert response.status_code == 400

def test_json_method_with_nested_json(simple_app):
    app_client = simple_app.test_client()
    data = json.dumps({"user": {"name": "John", "age": 30}, "active": True})
    response = app_client.post("/v1.0/forward", data=data, content_type='application/json')

    assert response.status_code == 200
    assert response.json() == json.loads(data)

def test_json_method_with_special_characters(simple_app):
    app_client = simple_app.test_client()
    data = json.dumps({"name": "John", "message": "Hello, world! @#$%^&*()"})
    response = app_client.post("/v1.0/forward", data=data, content_type='application/json')

    assert response.status_code == 200
    assert response.json() == json.loads(data)