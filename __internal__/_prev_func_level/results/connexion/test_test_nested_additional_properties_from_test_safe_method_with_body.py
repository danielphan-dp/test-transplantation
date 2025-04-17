def test_json_method_with_valid_data(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json-method",
        json={"key": "value"},
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 200
    response = resp.json()
    assert response == {"key": "value"}

def test_json_method_with_empty_data(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json-method",
        json={},
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 200
    response = resp.json()
    assert response == {}

def test_json_method_with_invalid_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json-method",
        data="invalid json",
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 400

def test_json_method_with_nested_data(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json-method",
        json={"nested": {"object": True}},
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 200
    response = resp.json()
    assert response == {"nested": {"object": True}}

def test_json_method_with_large_data(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    large_data = {"key": "value" * 1000}
    resp = app_client.post(
        "/v1.0/test-json-method",
        json=large_data,
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 200
    response = resp.json()
    assert response == large_data