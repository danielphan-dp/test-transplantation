def test_post_method_with_valid_data(problem_app):
    app_client = problem_app.test_client()
    response = app_client.post("/v1.0/post", json={"key": "value"})
    assert response.status_code == 201
    assert response.json() == {"key": "value", "name": "post"}

def test_post_method_with_empty_data(problem_app):
    app_client = problem_app.test_client()
    response = app_client.post("/v1.0/post", json={})
    assert response.status_code == 201
    assert response.json() == {"name": "post"}

def test_post_method_with_invalid_content_type(problem_app):
    app_client = problem_app.test_client()
    response = app_client.post("/v1.0/post", data="<html></html>", content_type="text/html")
    assert response.status_code == 415
    error_response = response.json()
    assert error_response["type"] == "about:blank"
    assert error_response["title"] == "Unsupported Media Type"
    assert error_response["detail"].startswith("Invalid Content-type (text/html)")
    assert error_response["status"] == 415

def test_post_method_with_missing_key(problem_app):
    app_client = problem_app.test_client()
    response = app_client.post("/v1.0/post", json={"name": "post"})
    assert response.status_code == 201
    assert response.json() == {"name": "post"}

def test_post_method_with_additional_keys(problem_app):
    app_client = problem_app.test_client()
    response = app_client.post("/v1.0/post", json={"key": "value", "extra": "data"})
    assert response.status_code == 201
    assert response.json() == {"key": "value", "extra": "data", "name": "post"}