import pytest
from connexion import FlaskApp
from connexion.resolver import MethodResolver
from conftest import build_app_from_fixture

def test_post_method_integration(spec, app_class):
    method_view_app = build_app_from_fixture(
        "method_view",
        app_class=app_class,
        spec_file=spec,
        resolver=MethodResolver("fakeapi.example_method_class"),
    )

    client = method_view_app.test_client()

    # Test valid post request
    r = client.post("/v1.0/pets", json={"name": "Musti"})
    assert r.json() == {"name": "post", "body": {"name": "Musti"}}

    # Test post request with missing body
    r = client.post("/v1.0/pets", json={})
    assert r.json() == {"name": "post", "body": {}}

    # Test post request with additional parameters
    r = client.post("/v1.0/pets", json={"name": "Musti", "extra": "value"})
    assert r.json() == {"name": "post", "body": {"name": "Musti", "extra": "value"}}

    # Test post request with invalid data type
    r = client.post("/v1.0/pets", json={"name": 123})
    assert r.status_code == 400  # Assuming the API returns a 400 for invalid types

    # Test post request with large payload
    large_payload = {"name": "A" * 1000}
    r = client.post("/v1.0/pets", json=large_payload)
    assert r.json() == {"name": "post", "body": large_payload}