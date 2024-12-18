def test_post_method(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}

    # Test with valid input
    valid_input = {"key": "value"}
    response = app_client.post("/v1.0/post", json=valid_input, headers=headers)
    assert response.status_code == 201
    assert response.headers.get("content-type") == "application/json"
    assert response.json() == {"key": "value", "name": "post"}

    # Test with empty input
    empty_input = {}
    response = app_client.post("/v1.0/post", json=empty_input, headers=headers)
    assert response.status_code == 201
    assert response.headers.get("content-type") == "application/json"
    assert response.json() == {"name": "post"}

    # Test with invalid input type
    invalid_input = 42
    response = app_client.post("/v1.0/post", json=invalid_input, headers=headers)
    assert response.status_code == 400  # Assuming the endpoint should return 400 for invalid input

    # Test with missing required fields (if applicable)
    missing_field_input = {"name": None}
    response = app_client.post("/v1.0/post", json=missing_field_input, headers=headers)
    assert response.status_code == 400  # Assuming the endpoint should return 400 for missing required fields

    # Test with additional unexpected fields
    additional_field_input = {"key": "value", "extra": "unexpected"}
    response = app_client.post("/v1.0/post", json=additional_field_input, headers=headers)
    assert response.status_code == 201
    assert response.headers.get("content-type") == "application/json"
    assert response.json() == {"key": "value", "extra": "unexpected", "name": "post"}