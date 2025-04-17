def test_post_method_with_valid_data(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.post("/v1.0/post", json={"key": "value"})
    assert response.status_code == 201
    assert response.json() == {"key": "value", "name": "post"}

def test_post_method_with_empty_data(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.post("/v1.0/post", json={})
    assert response.status_code == 201
    assert response.json() == {"name": "post"}

def test_post_method_with_invalid_data(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.post("/v1.0/post", data="invalid_data")
    assert response.status_code == 400  # Assuming the endpoint should return a 400 for invalid data

def test_post_method_with_missing_key(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.post("/v1.0/post", json={"name": "post"})
    assert response.status_code == 201
    assert response.json() == {"name": "post"}

def test_post_method_with_additional_keys(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.post("/v1.0/post", json={"key": "value", "extra": "data"})
    assert response.status_code == 201
    assert response.json() == {"key": "value", "extra": "data", "name": "post"}