def test_post_method(schema_app):
    app_client = schema_app.test_client()

    # Test with no arguments
    response_no_args = app_client.post("/v1.0/test_post")
    assert response_no_args.status_code == 201
    assert response_no_args.json() == {'name': 'post'}

    # Test with additional valid arguments
    response_with_args = app_client.post("/v1.0/test_post", json={"arg1": "value1", "arg2": "value2"})
    assert response_with_args.status_code == 201
    assert response_with_args.json() == {'arg1': 'value1', 'arg2': 'value2', 'name': 'post'}

    # Test with invalid argument types
    response_invalid_type = app_client.post("/v1.0/test_post", json={"arg1": 123})
    assert response_invalid_type.status_code == 400
    assert response_invalid_type.headers.get("content-type") == "application/problem+json"
    invalid_response_json = response_invalid_type.json()
    assert invalid_response_json["title"] == "Bad Request"
    assert invalid_response_json["detail"].startswith("123 is not of type 'string'")

    # Test with missing required properties
    response_missing_property = app_client.post("/v1.0/test_post", json={"arg2": "value2"})
    assert response_missing_property.status_code == 400
    assert response_missing_property.headers.get("content-type") == "application/problem+json"
    missing_property_response_json = response_missing_property.json()
    assert missing_property_response_json["title"] == "Bad Request"
    assert missing_property_response_json["detail"].startswith("'arg1' is a required property")

    # Test with unexpected properties
    response_unexpected_property = app_client.post("/v1.0/test_post", json={"arg1": "value1", "unexpected": "value"})
    assert response_unexpected_property.status_code == 201
    assert response_unexpected_property.json() == {'arg1': 'value1', 'unexpected': 'value', 'name': 'post'}