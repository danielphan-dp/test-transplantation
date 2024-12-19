import json
import pytest
from io import BytesIO

def test_json_method(simple_app):
    app_client = simple_app.test_client()
    
    # Test with empty string
    resp = app_client.post("/v1.0/nullable-parameters", data={"post_param": ""})
    assert resp.json() == "it was None"
    
    # Test with invalid JSON
    resp = app_client.put("/v1.0/nullable-parameters", content="invalid_json", headers={"Content-Type": "application/json"})
    assert resp.status_code == 400  # Expecting a bad request
    
    # Test with valid JSON but unexpected structure
    resp = app_client.put("/v1.0/nullable-parameters", content=json.dumps({"unexpected_key": "value"}), headers={"Content-Type": "application/json"})
    assert resp.json() != "it was None"  # Expecting a different response
    
    # Test with a large number
    large_number = 999999999999999999
    resp = app_client.get(f"/v1.0/nullable-parameters?time_start={large_number}")
    assert resp.json() == large_number
    
    # Test with boolean values
    resp = app_client.post("/v1.0/nullable-parameters", data={"post_param": "true"})
    assert resp.json() == "it was None"
    
    resp = app_client.post("/v1.0/nullable-parameters", data={"post_param": "false"})
    assert resp.json() == "it was None"