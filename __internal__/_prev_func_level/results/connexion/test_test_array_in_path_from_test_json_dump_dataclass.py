import json
import pytest

def test_json_empty_string(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-array-in-path/")
    assert resp.json() == []

def test_json_invalid_format(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-array-in-path/invalid_format")
    assert resp.status_code == 400

def test_json_multiple_items(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-array-in-path/item1,item2,item3")
    assert resp.json() == ["item1", "item2", "item3"]

def test_json_special_characters(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-array-in-path/item_with_special_characters_!@#")
    assert resp.json() == ["item_with_special_characters_!@#"]

def test_json_numeric_items(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-array-in-path/1,2,3")
    assert resp.json() == ["1", "2", "3"]