import json
import pytest
from conftest import TEST_FOLDER

@pytest.mark.parametrize('input_data, expected_output', [
    ({"key1": "value1"}, {"key1": "value1", "name": "post"}),
    ({"key2": "value2"}, {"key2": "value2", "name": "post"}),
    ({"key3": "value3", "key4": "value4"}, {"key3": "value3", "key4": "value4", "name": "post"}),
])
def test_post_method_with_kwargs(app_class, input_data, expected_output):
    app = app_class(__name__)
    app_client = app.test_client()

    response = app_client.post("/v1.0/post", json=input_data)
    assert response.status_code == 201
    assert response.json() == expected_output

def test_post_method_without_kwargs(app_class):
    app = app_class(__name__)
    app_client = app.test_client()

    response = app_client.post("/v1.0/post")
    assert response.status_code == 201
    assert response.json() == {"name": "post"}

def test_post_method_with_empty_kwargs(app_class):
    app = app_class(__name__)
    app_client = app.test_client()

    response = app_client.post("/v1.0/post", json={})
    assert response.status_code == 201
    assert response.json() == {"name": "post"}