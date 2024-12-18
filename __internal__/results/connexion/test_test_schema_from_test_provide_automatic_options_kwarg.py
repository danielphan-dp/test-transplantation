def test_post_method(schema_app):
    app_client = schema_app.test_client()

    # Test with no arguments
    empty_request = app_client.post("/v1.0/post_method", json={})
    assert empty_request.status_code == 400
    assert empty_request.headers.get("content-type") == "application/problem+json"
    empty_request_response = empty_request.json()
    assert empty_request_response["title"] == "Bad Request"
    assert empty_request_response["detail"].startswith("'name' is a required property")

    # Test with invalid data type
    invalid_request = app_client.post("/v1.0/post_method", json={"name": 123})
    assert invalid_request.status_code == 400
    assert invalid_request.headers.get("content-type") == "application/problem+json"
    invalid_request_response = invalid_request.json()
    assert invalid_request_response["title"] == "Bad Request"
    assert invalid_request_response["detail"].startswith("123 is not of type 'string'")

    # Test with valid data
    valid_request = app_client.post("/v1.0/post_method", json={"name": "valid_name"})
    assert valid_request.status_code == 201
    valid_request_response = valid_request.json()
    assert valid_request_response["name"] == "valid_name"

    # Test with additional unexpected data
    extra_data_request = app_client.post("/v1.0/post_method", json={"name": "valid_name", "extra": "data"})
    assert extra_data_request.status_code == 201
    extra_data_request_response = extra_data_request.json()
    assert extra_data_request_response["name"] == "valid_name"

    # Test with wrong content type
    wrong_type_request = app_client.post("/v1.0/post_method", data="invalid_data")
    assert wrong_type_request.status_code == 400
    assert wrong_type_request.headers.get("content-type") == "application/problem+json"
    wrong_type_response = wrong_type_request.json()
    assert wrong_type_response["title"] == "Bad Request"
    assert wrong_type_response["detail"].startswith("Invalid JSON")