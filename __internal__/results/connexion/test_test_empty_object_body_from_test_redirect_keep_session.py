def test_post_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-post",
        json={"key": "value"},
    )
    assert resp.status_code == 201
    response = resp.json()
    assert response["key"] == "value"
    assert response["name"] == "post"

def test_post_with_empty_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-post",
        json={},
    )
    assert resp.status_code == 201
    response = resp.json()
    assert response == {"name": "post"}

def test_post_with_additional_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-post",
        json={"extra": "data"},
    )
    assert resp.status_code == 201
    response = resp.json()
    assert response["extra"] == "data"
    assert response["name"] == "post"

def test_post_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-post",
        data="invalid json",
    )
    assert resp.status_code == 400  # Assuming the endpoint returns 400 for invalid JSON

def test_post_with_missing_key(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-post",
        json={"name": None},
    )
    assert resp.status_code == 201
    response = resp.json()
    assert response["name"] == "post"