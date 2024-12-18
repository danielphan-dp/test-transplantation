def test_json_method(schema_app):
    app_client = schema_app.test_client()

    # Test with empty string
    empty_string_request = app_client.post("/v1.0/test_schema", json="")
    assert empty_string_request.status_code == 400
    assert empty_string_request.headers.get("content-type") == "application/problem+json"
    empty_string_response = empty_string_request.json()
    assert empty_string_response["title"] == "Bad Request"
    assert empty_string_response["detail"].startswith("'' is not of type 'object'")

    # Test with invalid JSON
    invalid_json_request = app_client.post("/v1.0/test_schema", data="invalid json")
    assert invalid_json_request.status_code == 400
    assert invalid_json_request.headers.get("content-type") == "application/problem+json"
    invalid_json_response = invalid_json_request.json()
    assert invalid_json_response["title"] == "Bad Request"
    assert invalid_json_response["detail"].startswith("Expecting value")

    # Test with valid JSON but missing required fields
    missing_field_request = app_client.post("/v1.0/test_schema", json={"extra": "data"})
    assert missing_field_request.status_code == 400
    assert missing_field_request.headers.get("content-type") == "application/problem+json"
    missing_field_response = missing_field_request.json()
    assert missing_field_response["title"] == "Bad Request"
    assert missing_field_response["detail"].startswith("'image_version' is a required property")

    # Test with valid JSON and additional fields
    valid_request_with_extra = app_client.post("/v1.0/test_schema", json={"image_version": "version", "extra_field": "extra_value"})
    assert valid_request_with_extra.status_code == 200
    valid_request_with_extra_response = valid_request_with_extra.json()
    assert valid_request_with_extra_response["image_version"] == "version"
    assert valid_request_with_extra_response.get("extra_field") == "extra_value"

    # Test with nested JSON
    nested_json_request = app_client.post("/v1.0/test_schema", json={"image_version": "version", "nested": {"key": "value"}})
    assert nested_json_request.status_code == 200
    nested_json_response = nested_json_request.json()
    assert nested_json_response["image_version"] == "version"
    assert nested_json_response["nested"]["key"] == "value"