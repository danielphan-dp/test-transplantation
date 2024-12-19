import json
from io import BytesIO
import pytest

def test_json_method_with_valid_text(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-formData-multiple-file-upload",
        data={"text": json.dumps({"key": "value"})}
    )
    assert resp.status_code == 200
    assert resp.json() == {"key": "value"}

def test_json_method_with_empty_text(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-formData-multiple-file-upload",
        data={"text": ""}
    )
    assert resp.status_code == 200
    assert resp.json() == {}

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-formData-multiple-file-upload",
        data={"text": "invalid json"}
    )
    assert resp.status_code == 400

def test_json_method_with_none_text(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-formData-multiple-file-upload",
        data={"text": None}
    )
    assert resp.status_code == 400

def test_json_method_with_large_json(simple_app):
    app_client = simple_app.test_client()
    large_data = json.dumps({"key": "value" * 1000})
    resp = app_client.post(
        "/v1.0/test-formData-multiple-file-upload",
        data={"text": large_data}
    )
    assert resp.status_code == 200
    assert resp.json() == {"key": "value" * 1000}