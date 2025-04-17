import pytest
from connexion import FlaskApp
from connexion.resolver import MethodResolver
from conftest import build_app_from_fixture

@pytest.fixture
def method_view_app(app_class):
    return build_app_from_fixture(
        "method_view",
        app_class=app_class,
        resolver=MethodResolver("fakeapi.example_method_class"),
    )

def test_put_method_with_valid_data(method_view_app):
    client = method_view_app.test_client()
    r = client.put("/v1.0/pets/1", json={"name": "Igor"})
    assert r.status_code == 201
    assert r.json == {"name": "put", "petId": 1, "body": {"name": "Igor"}}

def test_put_method_with_empty_body(method_view_app):
    client = method_view_app.test_client()
    r = client.put("/v1.0/pets/1", json={})
    assert r.status_code == 201
    assert r.json == {"name": "put", "petId": 1, "body": {}}

def test_put_method_with_nonexistent_pet(method_view_app):
    client = method_view_app.test_client()
    r = client.put("/v1.0/pets/999", json={"name": "NonExistent"})
    assert r.status_code == 404  # Assuming the API returns 404 for non-existent pets

def test_put_method_with_invalid_data(method_view_app):
    client = method_view_app.test_client()
    r = client.put("/v1.0/pets/1", json={"invalid_field": "value"})
    assert r.status_code == 400  # Assuming the API returns 400 for invalid data

def test_put_method_without_body(method_view_app):
    client = method_view_app.test_client()
    r = client.put("/v1.0/pets/1")
    assert r.status_code == 400  # Assuming the API requires a body for PUT requests

def test_put_method_with_special_characters(method_view_app):
    client = method_view_app.test_client()
    r = client.put("/v1.0/pets/1", json={"name": "!@#$%^&*()"})
    assert r.status_code == 201
    assert r.json == {"name": "put", "petId": 1, "body": {"name": "!@#$%^&*()"}}