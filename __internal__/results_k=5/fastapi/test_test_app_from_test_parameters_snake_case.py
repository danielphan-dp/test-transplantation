import pytest
from docs_src.app_testing.app_b_an_py310 import test_main

@needs_py310
def test_create_item_with_missing_name(client: TestClient):
    response = client.post("/items/", json={"price": 10.0})
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Field required"

@needs_py310
def test_create_item_with_invalid_price(client: TestClient):
    response = client.post("/items/", json={"name": "Plumbus", "price": "invalid"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "value is not a valid float"

@needs_py310
def test_create_item_with_extra_fields(client: TestClient):
    response = client.post("/items/", json={"name": "Plumbus", "price": 10.0, "extra_field": "extra_value"})
    assert response.status_code == 200
    assert response.json() == {"name": "Plumbus", "description": None, "price": 10.0, "tax": None}

@needs_py310
def test_create_item_with_none_price(client: TestClient):
    response = client.post("/items/", json={"name": "Plumbus", "price": None})
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "none is not an allowed value"

@needs_py310
def test_create_item_with_sub_field(client: TestClient):
    data = {
        "name": "Plumbus",
        "sub": {"subname": "SubPlumbus", "sub_description": "Sub WTF"}
    }
    response = client.post("/items/", json=data)
    assert response.status_code == 200
    assert response.json() == {
        "name": "Plumbus",
        "description": None,
        "sub": {"subname": "SubPlumbus", "sub_description": "Sub WTF", "tags": []}
    }