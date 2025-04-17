def test_json_method_empty_string(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}

    empty_request = app_client.post(
        "/v1.0/test_json_method_empty_string",
        headers=headers,
        data=""
    )
    assert empty_request.status_code == 400
    empty_response = empty_request.json()
    assert "error" in empty_response

def test_json_method_invalid_json(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}

    invalid_json_request = app_client.post(
        "/v1.0/test_json_method_invalid_json",
        headers=headers,
        data="invalid_json"
    )
    assert invalid_json_request.status_code == 400
    invalid_response = invalid_json_request.json()
    assert "error" in invalid_response

def test_json_method_valid_json(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}

    valid_json_request = app_client.post(
        "/v1.0/test_json_method_valid_json",
        headers=headers,
        data='{"key": "value"}'
    )
    assert valid_json_request.status_code == 200
    valid_response = valid_json_request.json()
    assert valid_response["key"] == "value"

def test_json_method_missing_key(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}

    missing_key_request = app_client.post(
        "/v1.0/test_json_method_missing_key",
        headers=headers,
        data='{"another_key": "value"}'
    )
    assert missing_key_request.status_code == 400
    missing_key_response = missing_key_request.json()
    assert "error" in missing_key_response
    assert missing_key_response["error"] == "Missing required key"