import pytest
from connexion.FlaskApp import FlaskApp
from connexion.resolver.MethodViewResolver import MethodViewResolver
from conftest import build_app_from_fixture

def test_put_method_view_resolver_integration(spec):
    method_view_app = build_app_from_fixture(
        "method_view",
        app_class=FlaskApp,
        spec_file=spec,
        resolver=MethodViewResolver("fakeapi.example_method_view"),
    )

    client = method_view_app.test_client()

    # Test valid PUT request with body
    r = client.put("/v1.0/pets/1", json={"name": "Igor"})
    assert r.json() == {"name": "put", "petId": 1, "body": {"name": "Igor"}}

    # Test PUT request with missing body
    r = client.put("/v1.0/pets/1")
    assert r.status_code == 400  # Assuming the API returns 400 for missing body

    # Test PUT request with invalid data
    r = client.put("/v1.0/pets/1", json={"invalid_key": "value"})
    assert r.status_code == 422  # Assuming the API returns 422 for validation errors

    # Test PUT request with empty body
    r = client.put("/v1.0/pets/1", json={})
    assert r.json() == {"name": "put", "petId": 1, "body": {}}

    # Test PUT request with additional parameters
    r = client.put("/v1.0/pets/1", json={"name": "Igor", "extra": "data"})
    assert r.json() == {"name": "put", "petId": 1, "body": {"name": "Igor", "extra": "data"}}