def test_post_method_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    
    # Test with no kwargs
    resp = app_client.post("/v1.0/post-method")
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post'}

    # Test with additional kwargs
    resp = app_client.post("/v1.0/post-method", json={"extra_param": "value"})
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post', 'extra_param': 'value'}

    # Test with multiple kwargs
    resp = app_client.post("/v1.0/post-method", json={"param1": "value1", "param2": "value2"})
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post', 'param1': 'value1', 'param2': 'value2'}

    # Test with empty kwargs
    resp = app_client.post("/v1.0/post-method", json={})
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post'}

    # Test with invalid data type
    resp = app_client.post("/v1.0/post-method", json={"param": None})
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post', 'param': None}