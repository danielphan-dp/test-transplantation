import pytest
from connexion import FlaskApp
from connexion.resolver.MethodViewResolver import MethodViewResolver
from conftest import build_app_from_fixture

@pytest.mark.parametrize("input_data, expected_output", [
    ({"name": "Musti"}, {"name": "post", "body": {"name": "Musti"}}),
    ({"name": "Fido"}, {"name": "post", "body": {"name": "Fido"}}),
    ({"name": ""}, {"name": "post", "body": {"name": ""}}),
    ({"name": None}, {"name": "post", "body": {"name": None}}),
])
def test_post_method_view_resolver_integration(input_data, expected_output, spec):
    method_view_app = build_app_from_fixture(
        "method_view",
        app_class=FlaskApp,
        spec_file=spec,
        resolver=MethodViewResolver("fakeapi.example_method_view"),
    )

    client = method_view_app.test_client()

    r = client.post("/v1.0/pets", json=input_data)
    assert r.json() == expected_output

def test_post_method_view_resolver_integration_no_body(spec):
    method_view_app = build_app_from_fixture(
        "method_view",
        app_class=FlaskApp,
        spec_file=spec,
        resolver=MethodViewResolver("fakeapi.example_method_view"),
    )

    client = method_view_app.test_client()

    r = client.post("/v1.0/pets")
    assert r.status_code == 400  # Assuming no body should return a 400 error

def test_post_method_view_resolver_integration_invalid_data(spec):
    method_view_app = build_app_from_fixture(
        "method_view",
        app_class=FlaskApp,
        spec_file=spec,
        resolver=MethodViewResolver("fakeapi.example_method_view"),
    )

    client = method_view_app.test_client()

    r = client.post("/v1.0/pets", json={"invalid_key": "value"})
    assert r.status_code == 400  # Assuming invalid data should return a 400 error