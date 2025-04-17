import json
import pytest
from typing import List

def test_json_method(simple_app):
    app_client = simple_app.test_client()
    headers = {"Content-type": "application/json"}
    
    # Test with valid JSON
    payload = {"key": "value"}
    response = app_client.post("/v1.0/test_json", headers=headers, json=payload)
    json_response = response.json()
    assert json_response == {"key": "value"}
    
    # Test with empty JSON
    response = app_client.post("/v1.0/test_json", headers=headers, json={})
    json_response = response.json()
    assert json_response == {}
    
    # Test with invalid JSON
    response = app_client.post("/v1.0/test_json", headers=headers, data="invalid json")
    assert response.status_code == 400  # Expecting a bad request
    
    # Test with nested JSON
    nested_payload = {"outer": {"inner": "value"}}
    response = app_client.post("/v1.0/test_json", headers=headers, json=nested_payload)
    json_response = response.json()
    assert json_response == {"outer": {"inner": "value"}}
    
    # Test with array in JSON
    array_payload = {"items": ["apple", "banana", "cherry"]}
    response = app_client.post("/v1.0/test_json", headers=headers, json=array_payload)
    json_response = response.json()
    assert json_response == {"items": ["apple", "banana", "cherry"]}