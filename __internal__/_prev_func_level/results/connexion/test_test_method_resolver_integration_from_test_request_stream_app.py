import pytest
from connexion.resolver import MethodResolver
from conftest import build_app_from_fixture

def test_put_method_integration(spec, app_class):
    method_view_app = build_app_from_fixture(
        "method_view",
        app_class=app_class,
        spec_file=spec,
        resolver=MethodResolver("fakeapi.example_method_class"),
    )

    client = method_view_app.test_client()

    # Test valid PUT request with body
    r = client.put("/v1.0/pets/1", json={"name": "Igor"})
    assert r.json() == {"name": "put", "petId": 1, "body": {"name": "Igor"}}

    # Test PUT request with missing body
    r = client.put("/v1.0/pets/1")
    assert r.status_code == 400  # Assuming the API returns 400 for missing body

    # Test PUT request with invalid data type
    r = client.put("/v1.0/pets/1", json={"name": 123})
    assert r.status_code == 422  # Assuming the API returns 422 for validation error

    # Test PUT request with additional unexpected fields
    r = client.put("/v1.0/pets/1", json={"name": "Igor", "unexpected_field": "value"})
    assert r.json() == {"name": "put", "petId": 1, "body": {"name": "Igor"}}  # Assuming it ignores unexpected fields

    # Test PUT request with valid data but different petId
    r = client.put("/v1.0/pets/2", json={"name": "Max"})
    assert r.json() == {"name": "put", "petId": 2, "body": {"name": "Max"}}