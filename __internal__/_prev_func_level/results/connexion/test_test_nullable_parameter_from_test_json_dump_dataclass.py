def test_json_method(simple_app):
    app_client = simple_app.test_client()
    
    # Test with valid JSON string
    resp = app_client.post("/v1.0/json-endpoint", json={"key": "value"})
    assert resp.json() == {"key": "value"}
    
    # Test with empty JSON
    resp = app_client.post("/v1.0/json-endpoint", json={})
    assert resp.json() == {}
    
    # Test with invalid JSON
    resp = app_client.post("/v1.0/json-endpoint", data="invalid json", content_type='application/json')
    assert resp.status_code == 400  # Expecting a bad request
    
    # Test with None value
    resp = app_client.post("/v1.0/json-endpoint", json={"key": None})
    assert resp.json() == {"key": None}
    
    # Test with nested JSON
    resp = app_client.post("/v1.0/json-endpoint", json={"nested": {"key": "value"}})
    assert resp.json() == {"nested": {"key": "value"}}
    
    # Test with array in JSON
    resp = app_client.post("/v1.0/json-endpoint", json={"array": [1, 2, 3]})
    assert resp.json() == {"array": [1, 2, 3]}