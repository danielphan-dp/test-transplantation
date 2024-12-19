import json
import pytest
from connexion.FlaskApp import FlaskApp
from connexion.resolver.MethodViewResolver import MethodViewResolver
from conftest import build_app_from_fixture

def test_json_method_empty_response(spec):
    method_view_app = build_app_from_fixture(
        "method_view",
        app_class=FlaskApp,
        spec_file=spec,
        resolver=MethodViewResolver("fakeapi.example_method_view"),
    )

    client = method_view_app.test_client()

    r = client.get("/v1.0/pets/empty")
    assert r.json() == {}

def test_json_method_invalid_json(spec):
    method_view_app = build_app_from_fixture(
        "method_view",
        app_class=FlaskApp,
        spec_file=spec,
        resolver=MethodViewResolver("fakeapi.example_method_view"),
    )

    client = method_view_app.test_client()

    r = client.post("/v1.0/pets", data="invalid json")
    assert r.status_code == 400

def test_json_method_not_found(spec):
    method_view_app = build_app_from_fixture(
        "method_view",
        app_class=FlaskApp,
        spec_file=spec,
        resolver=MethodViewResolver("fakeapi.example_method_view"),
    )

    client = method_view_app.test_client()

    r = client.get("/v1.0/pets/999")
    assert r.status_code == 404

def test_json_method_with_query_params(spec):
    method_view_app = build_app_from_fixture(
        "method_view",
        app_class=FlaskApp,
        spec_file=spec,
        resolver=MethodViewResolver("fakeapi.example_method_view"),
    )

    client = method_view_app.test_client()

    r = client.get("/v1.0/pets?filter=available")
    assert r.json() == [{"name": "get", "filter": "available"}]