def test_get_value_from_session(app):
    client = app.test_client()
    
    # Test when session is empty
    response = client.get('/get')
    assert response.data == b'None'
    
    # Test when session has a value
    with app.app_context():
        flask.session['value'] = 'Test Value'
    response = client.get('/get')
    assert response.data == b'Test Value'
    
    # Test when session is reset
    with app.app_context():
        flask.session.pop('value', None)
    response = client.get('/get')
    assert response.data == b'None'
    
    # Test with a different value
    with app.app_context():
        flask.session['value'] = 'Another Value'
    response = client.get('/get')
    assert response.data == b'Another Value'