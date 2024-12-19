import json
import pytest
from io import BytesIO
from typing import List

def test_empty_array_in_path(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-array-in-path/")
    assert resp.json() == []

def test_single_item_array_in_path(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-array-in-path/single_item")
    assert resp.json() == ["single_item"]

def test_multiple_items_array_in_path(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-array-in-path/item1,item2,item3")
    assert resp.json() == ["item1", "item2", "item3"]

def test_invalid_path(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-array-in-path/invalid_item,")
    assert resp.json() == ["invalid_item", ""]

def test_special_characters_in_path(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-array-in-path/item_with_special_characters_!@#")
    assert resp.json() == ["item_with_special_characters_!@#"]