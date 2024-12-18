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

    # Test valid post request
    r = client.post("/v1.0/pets", json={"name": "Musti"})
    assert r.json() == {"name": "post", "body": {"name": "Musti"}}

    # Test post request with missing body
    r = client.post("/v1.0/pets")
    assert r.status_code == 400  # Assuming the API returns 400 for missing body

    # Test post request with invalid data
    r = client.post("/v1.0/pets", json={"invalid_key": "value"})
    assert r.status_code == 400  # Assuming the API returns 400 for invalid data

    # Test post request with empty body
    r = client.post("/v1.0/pets", json={})
    assert r.status_code == 400  # Assuming the API returns 400 for empty body

    # Test post request with additional fields
    r = client.post("/v1.0/pets", json={"name": "Musti", "extra": "field"})
    assert r.json() == {"name": "post", "body": {"name": "Musti", "extra": "field"}}