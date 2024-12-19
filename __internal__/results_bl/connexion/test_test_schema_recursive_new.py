import json

def test_post_method(schema_app):
    app_client = schema_app.test_client()

    # Test with no arguments
    response_no_args = app_client.post("/v1.0/test_schema_recursive")
    assert response_no_args.status_code == 201
    assert response_no_args.json() == {'name': 'post'}

    # Test with additional valid arguments
    response_with_args = app_client.post("/v1.0/test_schema_recursive", json={"children": [], "extra": "data"})
    assert response_with_args.status_code == 201
    assert response_with_args.json() == {'children': [], 'extra': 'data', 'name': 'post'}

    # Test with invalid JSON structure
    response_invalid_json = app_client.post("/v1.0/test_schema_recursive", json="invalid_json")
    assert response_invalid_json.status_code == 400
    assert response_invalid_json.headers.get("content-type") == "application/problem+json"
    invalid_json_response = response_invalid_json.json()
    assert invalid_json_response["title"] == "Bad Request"
    assert invalid_json_response["detail"].startswith("Invalid JSON structure")

    # Test with empty JSON object
    response_empty_json = app_client.post("/v1.0/test_schema_recursive", json={})
    assert response_empty_json.status_code == 201
    assert response_empty_json.json() == {'name': 'post'}