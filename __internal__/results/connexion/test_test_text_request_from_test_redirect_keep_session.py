def test_post_method_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    
    # Test with no kwargs
    resp = app_client.post("/v1.0/post-method")
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post'}

    # Test with additional kwargs
    resp = app_client.post("/v1.0/post-method", json={'foo': 'bar', 'baz': 'qux'})
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post', 'foo': 'bar', 'baz': 'qux'}

    # Test with empty kwargs
    resp = app_client.post("/v1.0/post-method", json={})
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post'}

    # Test with unexpected data type
    resp = app_client.post("/v1.0/post-method", data="string_instead_of_json")
    assert resp.status_code == 400  # Assuming the endpoint expects JSON and returns 400 for invalid content type

    # Test with missing required fields if applicable
    resp = app_client.post("/v1.0/post-method", json={'foo': 'bar'})
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post', 'foo': 'bar'}  # Assuming 'baz' is not required