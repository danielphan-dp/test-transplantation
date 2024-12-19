import json
import pytest

def test_json_method_with_valid_text(schema_app):
    app_client = schema_app.test_client()
    resp = app_client.get("/v1.0/define_global_response")
    assert resp.json() == ["general", "list"]
    assert json.loads(resp.data) == ["general", "list"]

def test_json_method_with_empty_text(schema_app):
    app_client = schema_app.test_client()
    resp = app_client.get("/v1.0/empty_response")
    assert resp.json() == []
    assert json.loads(resp.data) == []

def test_json_method_with_invalid_json(schema_app):
    app_client = schema_app.test_client()
    resp = app_client.get("/v1.0/invalid_json_response")
    with pytest.raises(json.JSONDecodeError):
        json.loads(resp.data)

def test_json_method_with_non_json_text(schema_app):
    app_client = schema_app.test_client()
    resp = app_client.get("/v1.0/non_json_response")
    assert resp.data == b'This is not JSON' 
    with pytest.raises(json.JSONDecodeError):
        json.loads(resp.data)