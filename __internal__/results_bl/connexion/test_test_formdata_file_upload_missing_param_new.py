import json
import pytest
from io import BytesIO

def test_post_method_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-post-method",
        data={"param1": "value1", "param2": "value2"}
    )
    assert resp.status_code == 201, resp.text
    assert resp.json == {'name': 'post', 'param1': 'value1', 'param2': 'value2'}

def test_post_method_with_empty_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-post-method",
        data={}
    )
    assert resp.status_code == 201, resp.text
    assert resp.json == {'name': 'post'}

def test_post_method_with_missing_params(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-post-method",
        data={"param1": "value1"}
    )
    assert resp.status_code == 201, resp.text
    assert resp.json == {'name': 'post', 'param1': 'value1'}

def test_post_method_with_file_upload(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-post-method",
        files={"file": ("example.txt", BytesIO(b"file contents"))}
    )
    assert resp.status_code == 201, resp.text
    assert resp.json == {'name': 'post'}