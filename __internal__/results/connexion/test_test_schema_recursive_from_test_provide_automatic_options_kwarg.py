def test_post_method(schema_app):
    app_client = schema_app.test_client()

    # Test with valid input
    valid_input = {"key": "value"}
    response = app_client.post("/v1.0/post", json=valid_input)
    assert response.status_code == 201
    assert response.json() == {"key": "value", "name": "post"}

    # Test with empty input
    empty_input = {}
    response = app_client.post("/v1.0/post", json=empty_input)
    assert response.status_code == 201
    assert response.json() == {"name": "post"}

    # Test with invalid input type
    invalid_input = 123
    response = app_client.post("/v1.0/post", json=invalid_input)
    assert response.status_code == 400
    assert response.headers.get("content-type") == "application/problem+json"
    invalid_response = response.json()
    assert invalid_response["title"] == "Bad Request"
    assert invalid_response["detail"].startswith("123 is not of type 'object'")

    # Test with missing required fields (if applicable)
    missing_field_input = {"name": "post"}
    response = app_client.post("/v1.0/post", json=missing_field_input)
    assert response.status_code == 400
    assert response.headers.get("content-type") == "application/problem+json"
    missing_field_response = response.json()
    assert missing_field_response["title"] == "Bad Request"
    assert "missing required field" in missing_field_response["detail"]  # Adjust based on actual validation logic