import json
import pytest
from conftest import TEST_FOLDER

@pytest.mark.parametrize('input_data, expected_response', [
    ({"key1": "value1"}, {"key1": "value1", "name": "post"}),
    ({"key2": "value2"}, {"key2": "value2", "name": "post"}),
    ({"key3": "value3"}, {"key3": "value3", "name": "post"}),
])
def test_post_method_with_valid_data(app_class, input_data, expected_response):
    app = app_class(__name__)
    app_client = app.test_client()

    response = app_client.post("/v1.0/post", json=input_data)
    assert response.status_code == 201
    assert response.json == expected_response

def test_post_method_with_empty_data(app_class):
    app = app_class(__name__)
    app_client = app.test_client()

    response = app_client.post("/v1.0/post", json={})
    assert response.status_code == 201
    assert response.json == {"name": "post"}

def test_post_method_with_invalid_data(app_class):
    app = app_class(__name__)
    app_client = app.test_client()

    response = app_client.post("/v1.0/post", data="invalid_data")
    assert response.status_code == 400  # Assuming the endpoint returns 400 for invalid data

def test_post_method_with_missing_key(app_class):
    app = app_class(__name__)
    app_client = app.test_client()

    response = app_client.post("/v1.0/post", json={"key": None})
    assert response.status_code == 201
    assert response.json == {"key": None, "name": "post"}