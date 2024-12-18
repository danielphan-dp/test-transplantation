def test_get_value_from_session(app):
    client = app.test_client()
    
    # Test default value when session is empty
    response = client.get('/get')
    assert response.data.decode() == 'None'
    
    # Test setting a value in the session
    with client.session_transaction() as session:
        session['value'] = 'Test Value'
    
    # Test retrieving the value from session
    response = client.get('/get')
    assert response.data.decode() == 'Test Value'
    
    # Test clearing the session
    with client.session_transaction() as session:
        session.clear()
    
    # Test default value again after clearing session
    response = client.get('/get')
    assert response.data.decode() == 'None'