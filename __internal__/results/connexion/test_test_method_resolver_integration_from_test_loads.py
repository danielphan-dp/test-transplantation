import json
import pytest
from connexion.resolver import MethodResolver
from conftest import build_app_from_fixture

def test_json_method_integration(spec, app_class):
    method_view_app = build_app_from_fixture(
        "method_view",
        app_class=app_class,
        spec_file=spec,
        resolver=MethodResolver("fakeapi.example_method_class"),
    )

    client = method_view_app.test_client()

    # Test valid JSON response
    r = client.get("/v1.0/pets")
    assert r.json() == [{"name": "search"}]

    # Test valid JSON response for specific pet
    r = client.get("/v1.0/pets/1")
    assert r.json() == {"name": "get", "petId": 1}

    # Test posting valid JSON data
    r = client.post("/v1.0/pets", json={"name": "Musti"})
    assert r.json() == {"name": "post", "body": {"name": "Musti"}}

    # Test updating pet with valid JSON data
    r = client.put("/v1.0/pets/1", json={"name": "Igor"})
    assert r.json() == {"name": "put", "petId": 1, "body": {"name": "Igor"}}

    # Test invalid JSON response
    r = client.get("/v1.0/pets/invalid")
    assert r.status_code == 404

    # Test empty JSON response
    r = client.get("/v1.0/pets/empty")
    assert r.json() == {}

    # Test JSON decoding error
    r = client.post("/v1.0/pets", data="invalid json")
    assert r.status_code == 400
    assert "Invalid JSON" in r.json()["detail"]