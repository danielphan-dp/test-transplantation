import json
import pytest
from connexion.FlaskApp import FlaskApp
from connexion.resolver.MethodViewResolver import MethodViewResolver
from conftest import build_app_from_fixture

def test_json_method_integration(spec):
    method_view_app = build_app_from_fixture(
        "method_view",
        app_class=FlaskApp,
        spec_file=spec,
        resolver=MethodViewResolver("fakeapi.example_method_view"),
    )

    client = method_view_app.test_client()

    # Test valid JSON response
    r = client.get("/v1.0/pets")
    assert r.json() == [{"name": "get"}]

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
    r = client.post("/v1.0/pets", data="invalid json")
    assert r.status_code == 400

    # Test empty JSON response
    r = client.get("/v1.0/pets/999")
    assert r.status_code == 404

    # Test JSON decoding error
    r = client.post("/v1.0/pets", json={"name": None})
    assert r.status_code == 400
    assert r.json() == {"error": "Invalid input"}