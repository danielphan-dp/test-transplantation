import json
import pytest
from io import BytesIO

def test_json_method_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json",
        data=json.dumps({"key": "value"}),
        headers={"content-type": "application/json"},
    )

    assert resp.status_code == 200
    assert resp.json() == {"key": "value"}

def test_json_method_with_empty_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json",
        data=json.dumps({}),
        headers={"content-type": "application/json"},
    )

    assert resp.status_code == 200
    assert resp.json() == {}

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json",
        data="invalid json",
        headers={"content-type": "application/json"},
    )

    assert resp.status_code == 400

def test_json_method_with_file_upload(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json",
        data={"file": ("filename.txt", BytesIO(b"file contents"))},
        headers={"content-type": "multipart/form-data"},
    )

    assert resp.status_code == 200
    assert resp.json() == {
        "files": {
            "filename.txt": "file contents",
        },
    }