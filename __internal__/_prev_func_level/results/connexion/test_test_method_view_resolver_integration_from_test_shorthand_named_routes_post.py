import pytest
from connexion import FlaskApp
from connexion.resolver.MethodViewResolver import MethodViewResolver
from conftest import build_app_from_fixture

def test_post_method_view_resolver_integration(spec):
    method_view_app = build_app_from_fixture(
        "method_view",
        app_class=FlaskApp,
        spec_file=spec,
        resolver=MethodViewResolver("fakeapi.example_method_view"),
    )

    client = method_view_app.test_client()

    # Test valid post request with body
    r = client.post("/v1.0/pets", json={"name": "Buddy"})
    assert r.status_code == 201
    assert r.json() == {"name": "post", "body": {"name": "Buddy"}}

    # Test post request with missing body
    r = client.post("/v1.0/pets", json={})
    assert r.status_code == 201
    assert r.json() == {"name": "post", "body": {}}

    # Test post request with additional fields
    r = client.post("/v1.0/pets", json={"name": "Charlie", "age": 3})
    assert r.status_code == 201
    assert r.json() == {"name": "post", "body": {"name": "Charlie", "age": 3}}

    # Test post request with invalid data type
    r = client.post("/v1.0/pets", json={"name": 123})
    assert r.status_code == 400  # Assuming the API returns 400 for invalid types

    # Test post request with unexpected field
    r = client.post("/v1.0/pets", json={"name": "Max", "unexpected_field": "value"})
    assert r.status_code == 201
    assert r.json() == {"name": "post", "body": {"name": "Max", "unexpected_field": "value"}}