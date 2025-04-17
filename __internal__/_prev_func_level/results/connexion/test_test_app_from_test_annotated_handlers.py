import json
import pytest

@pytest.mark.parametrize("input_data, expected_output", [
    ('{"key": "value"}', {"key": "value"}),
    ('{"number": 123}', {"number": 123}),
    ('{"boolean": true}', {"boolean": True}),
    ('{"null_value": null}', {"null_value": None}),
    ('invalid json', None)  # Edge case for invalid JSON
])
def test_json_method(unordered_definition_app, input_data, expected_output):
    app_client = unordered_definition_app.test_client()
    response = app_client.post("/v1.0/json-endpoint", data=input_data, content_type='application/json')
    
    if expected_output is None:
        assert response.status_code == 400
        response_data = response.json()
        assert response_data["detail"].startswith("Invalid JSON")
    else:
        assert response.status_code == 200
        assert response.json() == expected_output