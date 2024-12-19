import json
import pytest

def test_json_method_with_empty_string(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/forward", json="")
    assert response.status_code == 400

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/forward", data="invalid json")
    assert response.status_code == 400

def test_json_method_with_large_data(simple_app):
    app_client = simple_app.test_client()
    large_data = {str(i): i for i in range(1000)}
    response = app_client.post("/v1.0/forward", json=large_data)
    assert response.status_code == 200
    assert response.json() == large_data

def test_json_method_with_special_characters(simple_app):
    app_client = simple_app.test_client()
    data = {
        "key_with_special_characters": "!@#$%^&*()_+[]{}|;':,.<>?/~`"
    }
    response = app_client.post("/v1.0/forward", json=data)
    assert response.status_code == 200
    assert response.json() == data

def test_json_method_with_nested_json(simple_app):
    app_client = simple_app.test_client()
    data = {
        "user": {
            "name": "John",
            "details": {
                "age": 30,
                "active": True
            }
        }
    }
    response = app_client.post("/v1.0/forward", json=data)
    assert response.status_code == 200
    assert response.json() == data

def test_json_method_with_non_serializable_data(simple_app):
    app_client = simple_app.test_client()
    data = {
        "key": set([1, 2, 3])
    }
    response = app_client.post("/v1.0/forward", json=data)
    assert response.status_code == 400