def test_post_method_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    url = "/v1.0/test_post_method"
    
    # Test with no kwargs
    response = app_client.post(url)
    assert response.status_code == 201
    assert response.json() == {'name': 'post'}

    # Test with single kwarg
    response = app_client.post(url, json={'key1': 'value1'})
    assert response.status_code == 201
    assert response.json() == {'key1': 'value1', 'name': 'post'}

    # Test with multiple kwargs
    response = app_client.post(url, json={'key1': 'value1', 'key2': 'value2'})
    assert response.status_code == 201
    assert response.json() == {'key1': 'value1', 'key2': 'value2', 'name': 'post'}

    # Test with empty kwargs
    response = app_client.post(url, json={})
    assert response.status_code == 201
    assert response.json() == {'name': 'post'}

    # Test with unexpected data type
    response = app_client.post(url, json={'key1': 123, 'key2': [1, 2, 3]})
    assert response.status_code == 201
    assert response.json() == {'key1': 123, 'key2': [1, 2, 3], 'name': 'post'}