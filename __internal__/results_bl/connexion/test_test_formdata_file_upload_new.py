import json
import pytest
from io import BytesIO

def test_json_method_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    
    resp = app_client.post(
        "/v1.0/test-formData-file-upload",
        files={"file": ("valid_file.txt", BytesIO(b"valid file contents"))},
    )
    assert resp.status_code == 200
    assert resp.json() == {"valid_file.txt": "valid file contents"}

def test_json_method_with_empty_file(simple_app):
    app_client = simple_app.test_client()
    
    resp = app_client.post(
        "/v1.0/test-formData-file-upload",
        files={"file": ("empty_file.txt", BytesIO(b""))},
    )
    assert resp.status_code == 200
    assert resp.json() == {"empty_file.txt": ""}

def test_json_method_with_invalid_file_type(simple_app):
    app_client = simple_app.test_client()
    
    resp = app_client.post(
        "/v1.0/test-formData-file-upload",
        files={"file": ("invalid_file.txt", BytesIO(b"invalid file contents"))},
    )
    assert resp.status_code == 200
    assert resp.json() == {"invalid_file.txt": "invalid file contents"}

def test_json_method_with_no_file(simple_app):
    app_client = simple_app.test_client()
    
    resp = app_client.post(
        "/v1.0/test-formData-file-upload",
        data={},
    )
    assert resp.status_code == 400

def test_json_method_with_multiple_files(simple_app):
    app_client = simple_app.test_client()
    
    resp = app_client.post(
        "/v1.0/test-formData-file-upload",
        files=[
            ("file", ("file1.txt", BytesIO(b"file1 contents"))),
            ("file", ("file2.txt", BytesIO(b"file2 contents"))),
        ],
    )
    assert resp.status_code == 400