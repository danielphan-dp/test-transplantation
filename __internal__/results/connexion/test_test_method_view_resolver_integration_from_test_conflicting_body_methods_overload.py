import pytest
from connexion.FlaskApp import FlaskApp
from connexion.resolver.MethodViewResolver import MethodViewResolver
from conftest import build_app_from_fixture

@pytest.fixture
def method_view_app(spec):
    app = build_app_from_fixture(
        "method_view",
        app_class=FlaskApp,
        spec_file=spec,
        resolver=MethodViewResolver("fakeapi.example_method_view"),
    )
    return app

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
    r = client.put("/v1.0/pets/999", json={"name": "Nonexistent"})
    assert r.status_code == 404  # Assuming the endpoint returns 404 for non-existent pets

def test_put_method_with_invalid_data(method_view_app):
    client = method_view_app.test_client()
    r = client.put("/v1.0/pets/1", json={"invalid_key": "value"})
    assert r.status_code == 400  # Assuming the endpoint returns 400 for invalid data

def test_put_method_without_json(method_view_app):
    client = method_view_app.test_client()
    r = client.put("/v1.0/pets/1")
    assert r.status_code == 400  # Assuming the endpoint requires JSON body and returns 400 if not provided