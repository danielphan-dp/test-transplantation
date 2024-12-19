import json
import pytest

def test_json_method_with_empty_string(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-bool-param", params={"thruthiness": ""})
    assert resp.status_code == 200
    response = resp.json()
    assert response is False

def test_json_method_with_invalid_boolean(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-bool-param", params={"thruthiness": "not_a_bool"})
    assert resp.status_code == 200
    response = resp.json()
    assert response is False

def test_json_method_with_none(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-bool-param", params={"thruthiness": None})
    assert resp.status_code == 200
    response = resp.json()
    assert response is False

def test_json_method_with_boolean_false(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-bool-param", params={"thruthiness": False})
    assert resp.status_code == 200
    response = resp.json()
    assert response is False

def test_json_method_with_boolean_true(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-bool-param", params={"thruthiness": True})
    assert resp.status_code == 200
    response = resp.json()
    assert response is True