def test_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()

    # Test with valid JSON string
    post_data = app_client.post(
        "/v1.0/json_endpoint",
        json={"text": '{"key": "value"}'},
    )
    assert post_data.status_code == 200
    assert post_data.headers.get("content-type") == "application/json"
    json_response = post_data.json()
    assert json_response["key"] == "value"

    # Test with invalid JSON string
    post_data = app_client.post(
        "/v1.0/json_endpoint",
        json={"text": '{"key": "value"'},
    )
    assert post_data.status_code == 400

    # Test with empty JSON string
    post_data = app_client.post(
        "/v1.0/json_endpoint",
        json={"text": ""},
    )
    assert post_data.status_code == 400

    # Test with non-JSON string
    post_data = app_client.post(
        "/v1.0/json_endpoint",
        json={"text": "not a json"},
    )
    assert post_data.status_code == 400

    # Test with valid JSON containing different data types
    post_data = app_client.post(
        "/v1.0/json_endpoint",
        json={"text": '{"int": 1, "float": 1.5, "bool": true, "null": null}'},
    )
    assert post_data.status_code == 200
    json_response = post_data.json()
    assert json_response["int"] == 1
    assert json_response["float"] == 1.5
    assert json_response["bool"] is True
    assert json_response["null"] is None