def test_post_method(schema_app):
    app_client = schema_app.test_client()

    # Test with no arguments
    response_no_args = app_client.post("/v1.0/post_method")
    assert response_no_args.status_code == 200
    assert response_no_args.json() == {'name': 'post'}

    # Test with additional arguments
    response_with_extra = app_client.post("/v1.0/post_method", json={"extra_param": "value"})
    assert response_with_extra.status_code == 200
    assert response_with_extra.json() == {'name': 'post', 'extra_param': 'value'}

    # Test with invalid data type
    response_invalid_type = app_client.post("/v1.0/post_method", json="invalid_data")
    assert response_invalid_type.status_code == 400
    assert response_invalid_type.headers.get("content-type") == "application/problem+json"
    invalid_type_response = response_invalid_type.json()
    assert invalid_type_response["title"] == "Bad Request"
    assert invalid_type_response["detail"].startswith('"invalid_data" is not of type')

    # Test with missing required fields (if applicable)
    response_missing_field = app_client.post("/v1.0/post_method", json={})
    assert response_missing_field.status_code == 400
    assert response_missing_field.headers.get("content-type") == "application/problem+json"
    missing_field_response = response_missing_field.json()
    assert missing_field_response["title"] == "Bad Request"
    assert missing_field_response["detail"].startswith("Required field is missing")

    # Test with valid data
    response_valid_data = app_client.post("/v1.0/post_method", json={"name": "valid_name"})
    assert response_valid_data.status_code == 200
    assert response_valid_data.json() == {'name': 'post', 'name': 'valid_name'}