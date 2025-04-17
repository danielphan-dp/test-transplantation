import json
import pytest
from connexion.FlaskApp import FlaskApp
from connexion.resolver.MethodViewResolver import MethodViewResolver
from conftest import build_app_from_fixture

@pytest.mark.parametrize("input_data, expected_output", [
    ('{"name": "get"}', {"name": "get"}),
    ('{"name": "get", "petId": 1}', {"name": "get", "petId": 1}),
    ('{"name": "post", "body": {"name": "Musti"}}', {"name": "post", "body": {"name": "Musti"}}),
    ('{"name": "put", "petId": 1, "body": {"name": "Igor"}}', {"name": "put", "petId": 1, "body": {"name": "Igor"}}),
    ('{"invalid_json": "missing closing brace"', None),  # Edge case: invalid JSON
])
def test_json_method_integration(input_data, expected_output):
    method_view_app = build_app_from_fixture(
        "method_view",
        app_class=FlaskApp,
        spec_file='spec',
        resolver=MethodViewResolver("fakeapi.example_method_view"),
    )

    client = method_view_app.test_client()

    if expected_output is None:
        response = client.post("/v1.0/pets", data=input_data, content_type='application/json')
        assert response.status_code == 400  # Expecting a bad request for invalid JSON
    else:
        response = client.post("/v1.0/pets", data=input_data, content_type='application/json')
        assert response.json() == expected_output