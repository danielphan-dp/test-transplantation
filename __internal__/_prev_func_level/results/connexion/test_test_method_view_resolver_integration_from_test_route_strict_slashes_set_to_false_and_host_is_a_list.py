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

    r = client.put("/v1.0/pets/1", json={"name": "Igor"})
    assert r.json() == {"name": "put", "petId": 1, "body": {"name": "Igor"}}

    r = client.put("/v1.0/pets/2", json={"name": "Max"})
    assert r.json() == {"name": "put", "petId": 2, "body": {"name": "Max"}}

    r = client.put("/v1.0/pets/3", json={})
    assert r.json() == {"name": "put", "petId": 3, "body": {}}

    r = client.put("/v1.0/pets/4", json={"name": None})
    assert r.json() == {"name": "put", "petId": 4, "body": {"name": None}}