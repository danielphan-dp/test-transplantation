import json

def test_post_method(schema_app):
    app_client = schema_app.test_client()

    # Test with no arguments
    response_no_args = app_client.post("/v1.0/test_schema_map")
    assert response_no_args.status_code == 201
    assert response_no_args.json() == {'name': 'post'}

    # Test with additional valid arguments
    response_with_args = app_client.post("/v1.0/test_schema_map", json={"foo": {"image_version": "string"}, "extra": "value"})
    assert response_with_args.status_code == 201
    assert response_with_args.json() == {'foo': {'image_version': 'string'}, 'extra': 'value', 'name': 'post'}

    # Test with empty JSON
    response_empty_json = app_client.post("/v1.0/test_schema_map", json={})
    assert response_empty_json.status_code == 201
    assert response_empty_json.json() == {'name': 'post'}

    # Test with non-JSON data
    response_non_json = app_client.post("/v1.0/test_schema_map", data="string data")
    assert response_non_json.status_code == 400
    assert response_non_json.headers.get("content-type") == "application/problem+json"
    non_json_response = response_non_json.json()
    assert non_json_response["title"] == "Bad Request"
    assert non_json_response["detail"].startswith("string data is not of type 'object'")