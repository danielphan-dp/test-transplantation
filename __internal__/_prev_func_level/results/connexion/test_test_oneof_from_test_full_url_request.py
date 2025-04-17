import pytest

def test_post_method(simple_openapi_app):
    app_client = simple_openapi_app.test_client()

    # Test with valid input
    post_response = app_client.post(
        "/v1.0/post_method",
        json={"name": "valid_name"},
    )
    assert post_response.status_code == 201
    assert post_response.headers.get("content-type") == "application/json"
    response_data = post_response.json()
    assert response_data["name"] == "valid_name"

    # Test with empty input
    post_response = app_client.post(
        "/v1.0/post_method",
        json={},
    )
    assert post_response.status_code == 201
    response_data = post_response.json()
    assert response_data["name"] == "post"

    # Test with numeric input
    post_response = app_client.post(
        "/v1.0/post_method",
        json={"name": 123},
    )
    assert post_response.status_code == 201
    response_data = post_response.json()
    assert response_data["name"] == 123

    # Test with boolean input
    post_response = app_client.post(
        "/v1.0/post_method",
        json={"name": False},
    )
    assert post_response.status_code == 201
    response_data = post_response.json()
    assert response_data["name"] == False

    # Test with invalid input type
    post_response = app_client.post(
        "/v1.0/post_method",
        json={"name": ["invalid", "type"]},
    )
    assert post_response.status_code == 400

    # Test with null input
    post_response = app_client.post(
        "/v1.0/post_method",
        json={"name": None},
    )
    assert post_response.status_code == 201
    response_data = post_response.json()
    assert response_data["name"] == None