def test_post_method(schema_app):
    app_client = schema_app.test_client()

    # Test with no kwargs
    response = app_client.post("/v1.0/post", json={})
    assert response.status_code == 201
    assert response.json() == {'name': 'post'}

    # Test with additional kwargs
    response = app_client.post("/v1.0/post", json={'extra': 'data'})
    assert response.status_code == 201
    assert response.json() == {'name': 'post', 'extra': 'data'}

    # Test with invalid data type
    response = app_client.post("/v1.0/post", json='invalid_data')
    assert response.status_code == 400  # Assuming the endpoint returns 400 for invalid JSON

    # Test with missing required fields (if any)
    response = app_client.post("/v1.0/post", json={})
    assert response.status_code == 201
    assert response.json() == {'name': 'post'}  # Assuming no required fields are enforced

    # Test with unexpected fields
    response = app_client.post("/v1.0/post", json={'unexpected': 'field'})
    assert response.status_code == 201
    assert response.json() == {'name': 'post', 'unexpected': 'field'}