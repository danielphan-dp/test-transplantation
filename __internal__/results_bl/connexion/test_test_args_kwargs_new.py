import json
import pytest

def test_json_method_with_empty_text(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/query-params-as-kwargs")
    assert resp.status_code == 200
    assert json.loads(resp.data) == {}

def test_json_method_with_valid_json(simple_app):
    app_client = simple_app.test_client()
    body = json.dumps({"foo": "a", "bar": "b"})
    resp = app_client.post("/v1.0/body-params-as-kwargs", data=body, content_type='application/json')
    assert resp.status_code == 200
    assert json.loads(resp.data) == {"body": {"foo": "a", "bar": "b"}}

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    body = "invalid json"
    resp = app_client.post("/v1.0/body-params-as-kwargs", data=body, content_type='application/json')
    assert resp.status_code == 400

def test_json_method_with_missing_key(simple_app):
    app_client = simple_app.test_client()
    body = json.dumps({"foo": "a"})
    resp = app_client.post("/v1.0/body-params-as-kwargs", data=body, content_type='application/json')
    assert resp.status_code == 200
    assert json.loads(resp.data) == {"body": {"foo": "a"}} 

def test_json_method_with_large_payload(simple_app):
    app_client = simple_app.test_client()
    body = json.dumps({"foo": "a" * 10000})
    resp = app_client.post("/v1.0/body-params-as-kwargs", data=body, content_type='application/json')
    assert resp.status_code == 200
    assert json.loads(resp.data) == {"body": {"foo": "a" * 10000}} 

def test_json_method_with_non_json_content(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/body-params-as-kwargs", data="text/plain", content_type='text/plain')
    assert resp.status_code == 415