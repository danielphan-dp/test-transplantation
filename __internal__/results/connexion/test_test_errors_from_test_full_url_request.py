import pytest

def test_post_method(problem_app):
    app_client = problem_app.test_client()

    # Test with no kwargs
    response = app_client.post("/v1.0/post")
    assert response.status_code == 201
    assert response.json() == {'name': 'post'}

    # Test with additional kwargs
    response = app_client.post("/v1.0/post", json={'extra': 'data'})
    assert response.status_code == 201
    assert response.json() == {'name': 'post', 'extra': 'data'}

    # Test with empty body
    response = app_client.post("/v1.0/post", json={})
    assert response.status_code == 201
    assert response.json() == {'name': 'post'}

    # Test with invalid content type
    response = app_client.post("/v1.0/post", data="<html></html>", headers={"content-type": "text/html"})
    assert response.status_code == 415
    assert response.json()["type"] == "about:blank"
    assert response.json()["title"] == "Unsupported Media Type"
    assert response.json()["detail"].startswith("Invalid Content-type (text/html)")
    assert response.json()["status"] == 415

    # Test with missing required fields (if applicable)
    response = app_client.post("/v1.0/post", json={'missing_field': 'value'})
    assert response.status_code == 400  # Assuming 400 for bad request
    assert response.json()["type"] == "about:blank"
    assert response.json()["title"] == "Bad Request"
    assert response.json()["status"] == 400

    # Test with unexpected fields
    response = app_client.post("/v1.0/post", json={'unexpected_field': 'value'})
    assert response.status_code == 201
    assert response.json() == {'name': 'post', 'unexpected_field': 'value'}