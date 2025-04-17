def test_post_method(schema_app):
    app_client = schema_app.test_client()

    # Test with no arguments
    response_no_args = app_client.post("/v1.0/post_method")
    assert response_no_args.status_code == 201
    assert response_no_args.json() == {'name': 'post'}

    # Test with additional valid arguments
    response_with_args = app_client.post("/v1.0/post_method", json={"foo": "bar"})
    assert response_with_args.status_code == 201
    assert response_with_args.json() == {'name': 'post', 'foo': 'bar'}

    # Test with invalid argument type
    response_invalid_type = app_client.post("/v1.0/post_method", json="invalid")
    assert response_invalid_type.status_code == 400
    assert response_invalid_type.headers.get("content-type") == "application/problem+json"
    invalid_response_json = response_invalid_type.json()
    assert invalid_response_json["title"] == "Bad Request"
    assert invalid_response_json["detail"].startswith('"invalid" is not of type')

    # Test with missing required fields
    response_missing_fields = app_client.post("/v1.0/post_method", json={})
    assert response_missing_fields.status_code == 201
    assert response_missing_fields.json() == {'name': 'post'}