import pytest
from docs_src.app_testing.app_b_an_py310 import test_main

@needs_py310
def test_create_item_with_missing_fields(client: TestClient):
    response = client.post("/items/", json={"name": "Foo"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "price"],
                "msg": "Field required",
                "input": {"name": "Foo"},
            }
        ]
    }

@needs_py310
def test_create_item_with_invalid_data_type(client: TestClient):
    response = client.post("/items/", json={"name": "Foo", "price": "not_a_number"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "type_error.float",
                "loc": ["body", "price"],
                "msg": "value is not a valid float",
                "input": "not_a_number",
            }
        ]
    }

@needs_py310
def test_create_item_with_extra_fields(client: TestClient):
    response = client.post("/items/", json={"name": "Foo", "price": 50.5, "extra_field": "extra_value"})
    assert response.status_code == 200
    assert response.json() == {
        "name": "Foo",
        "description": None,
        "price": 50.5,
        "extra_field": "extra_value"
    }

@needs_py310
def test_create_item_with_sub_field(client: TestClient):
    data = {
        "name": "Plumbus",
        "sub": {"subname": "SubPlumbus", "sub_description": "Sub WTF"},
    }
    response = client.post("/items/", json=data)
    assert response.status_code == 200
    assert response.json() == {
        "name": "Plumbus",
        "description": None,
        "sub": {"subname": "SubPlumbus", "sub_description": "Sub WTF", "tags": []},
    }