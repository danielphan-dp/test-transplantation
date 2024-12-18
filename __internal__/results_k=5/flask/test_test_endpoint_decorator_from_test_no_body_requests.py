def test_get_endpoint_with_session_value(app, client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_endpoint_without_session_value(app, client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_endpoint_with_none_session_value(app, client):
    with client.session_transaction() as session:
        session['value'] = None
    
    response = client.get('/get')
    assert response.data == b'None'