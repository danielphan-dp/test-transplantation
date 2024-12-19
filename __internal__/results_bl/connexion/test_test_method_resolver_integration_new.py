import json
import pytest
from connexion.FlaskApp import FlaskApp
from connexion.operations.OpenAPIOperation import OpenAPIOperation
from connexion.resolver.MethodResolver import MethodResolver
from connexion.resolver.MethodViewResolver import MethodViewResolver
from connexion.resolver.Resolver import Resolver
from conftest import build_app_from_fixture

def test_json_method_empty_response(spec, app_class):
    method_view_app = build_app_from_fixture(
        "method_view",
        app_class=app_class,
        spec_file=spec,
        resolver=MethodResolver("fakeapi.example_method_class"),
    )

    client = method_view_app.test_client()

    r = client.get("/v1.0/pets/empty")
    assert r.json() == {}

def test_json_method_invalid_json(spec, app_class):
    method_view_app = build_app_from_fixture(
        "method_view",
        app_class=app_class,
        spec_file=spec,
        resolver=MethodResolver("fakeapi.example_method_class"),
    )

    client = method_view_app.test_client()

    r = client.post("/v1.0/pets", data="invalid json")
    assert r.status_code == 400

def test_json_method_not_found(spec, app_class):
    method_view_app = build_app_from_fixture(
        "method_view",
        app_class=app_class,
        spec_file=spec,
        resolver=MethodResolver("fakeapi.example_method_class"),
    )

    client = method_view_app.test_client()

    r = client.get("/v1.0/pets/999")
    assert r.status_code == 404

def test_json_method_with_additional_fields(spec, app_class):
    method_view_app = build_app_from_fixture(
        "method_view",
        app_class=app_class,
        spec_file=spec,
        resolver=MethodResolver("fakeapi.example_method_class"),
    )

    client = method_view_app.test_client()

    r = client.post("/v1.0/pets", json={"name": "Musti", "age": 5})
    assert r.json() == {"name": "post", "body": {"name": "Musti", "age": 5}}