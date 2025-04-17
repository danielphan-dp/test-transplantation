def test_post_with_valid_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-post",
        json={"key1": "value1", "key2": "value2"},
    )
    assert resp.status_code == 201
    response = resp.json()
    assert response["key1"] == "value1"
    assert response["key2"] == "value2"
    assert response["name"] == "post"

def test_post_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-post",
        json={},
    )
    assert resp.status_code == 201
    response = resp.json()
    assert response == {"name": "post"}

def test_post_with_additional_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-post",
        json={"extra_key": "extra_value"},
    )
    assert resp.status_code == 201
    response = resp.json()
    assert response["extra_key"] == "extra_value"
    assert response["name"] == "post"

def test_post_with_invalid_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-post",
        json="invalid_data",
    )
    assert resp.status_code == 400  # Assuming the endpoint should return a 400 for invalid JSON

def test_post_with_missing_body(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-post",
    )
    assert resp.status_code == 400  # Assuming the endpoint should return a 400 for missing body