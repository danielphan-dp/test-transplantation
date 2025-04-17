import pytest

def test_post_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    data = {
        "name": "Alice",
        "age": 30,
        "city": "Wonderland"
    }
    response = app_client.post("/v1.0/forward", json=data)

    assert response.status_code == 201
    assert response.json() == {"name": "post", "age": 30, "city": "Wonderland"}

def test_post_with_empty_data(simple_app):
    app_client = simple_app.test_client()
    data = {}
    response = app_client.post("/v1.0/forward", json=data)

    assert response.status_code == 201
    assert response.json() == {"name": "post"}

def test_post_with_special_characters(simple_app):
    app_client = simple_app.test_client()
    data = {
        "name": "John",
        "$surname": "Doe",
        "1337": True,
        "!#/bin/sh": False
    }
    response = app_client.post("/v1.0/forward", json=data)

    assert response.status_code == 201
    assert response.json() == {"name": "post", "$surname": "Doe", "1337": True, "!#/bin/sh": False}

def test_post_with_large_data(simple_app):
    app_client = simple_app.test_client()
    data = {f"key_{i}": f"value_{i}" for i in range(1000)}
    response = app_client.post("/v1.0/forward", json=data)

    assert response.status_code == 201
    assert response.json() == {**data, "name": "post"}

def test_post_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/forward", data="invalid json")

    assert response.status_code == 400  # Assuming the endpoint returns 400 for invalid JSON

def test_post_with_missing_name(simple_app):
    app_client = simple_app.test_client()
    data = {
        "age": 25,
        "city": "Nowhere"
    }
    response = app_client.post("/v1.0/forward", json=data)

    assert response.status_code == 201
    assert response.json() == {"name": "post", "age": 25, "city": "Nowhere"}