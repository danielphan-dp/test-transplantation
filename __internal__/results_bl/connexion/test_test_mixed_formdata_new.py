import json
import pytest
from io import BytesIO

def test_json_method_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-mixed-formData",
        data={"formData": "test"},
        files={"file": ("filename.txt", BytesIO(b"file contents"))},
    )
    assert resp.status_code == 200
    assert resp.json() == {
        "data": {"formData": "test"},
        "files": {
            "filename.txt": "file contents",
        },
    }

def test_json_method_with_empty_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-mixed-formData",
        data={},
        files={"file": ("filename.txt", BytesIO(b"file contents"))},
    )
    assert resp.status_code == 200
    assert resp.json() == {
        "data": {},
        "files": {
            "filename.txt": "file contents",
        },
    }

def test_json_method_with_no_files(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-mixed-formData",
        data={"formData": "test"},
        files={},
    )
    assert resp.status_code == 200
    assert resp.json() == {
        "data": {"formData": "test"},
        "files": {},
    }

def test_json_method_with_large_file(simple_app):
    app_client = simple_app.test_client()
    large_file_content = b"a" * (10**6)  # 1 MB file
    resp = app_client.post(
        "/v1.0/test-mixed-formData",
        data={"formData": "test"},
        files={"file": ("largefile.txt", BytesIO(large_file_content))},
    )
    assert resp.status_code == 200
    assert resp.json() == {
        "data": {"formData": "test"},
        "files": {
            "largefile.txt": "a" * (10**6),
        },
    }

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-mixed-formData",
        data={"formData": "test"},
        files={"file": ("filename.txt", BytesIO(b"invalid contents"))},
    )
    assert resp.status_code == 200
    assert resp.json() == {
        "data": {"formData": "test"},
        "files": {
            "filename.txt": "invalid contents",
        },
    }