import json
import pytest

def test_json_method(schema_app):
    app_client = schema_app.test_client()

    valid_json_string = '{"key": "value", "number": 123}'
    invalid_json_string = '{"key": "value", "number": }'
    malformed_json_string = '{"key": "value", "number": 123'

    # Test valid JSON input
    response_valid = app_client.post("/v1.0/test_json_method", data=valid_json_string, content_type='application/json')
    assert response_valid.status_code == 200
    assert response_valid.json() == json.loads(valid_json_string)

    # Test invalid JSON input (missing value)
    response_invalid = app_client.post("/v1.0/test_json_method", data=invalid_json_string, content_type='application/json')
    assert response_invalid.status_code == 400
    assert response_invalid.headers.get("content-type") == "application/problem+json"
    invalid_response_data = response_invalid.json()
    assert invalid_response_data["title"] == "Bad Request"
    assert invalid_response_data["detail"].startswith("Expecting value")

    # Test malformed JSON input
    response_malformed = app_client.post("/v1.0/test_json_method", data=malformed_json_string, content_type='application/json')
    assert response_malformed.status_code == 400
    assert response_malformed.headers.get("content-type") == "application/problem+json"
    malformed_response_data = response_malformed.json()
    assert malformed_response_data["title"] == "Bad Request"
    assert malformed_response_data["detail"].startswith("Expecting ',' or '}'")