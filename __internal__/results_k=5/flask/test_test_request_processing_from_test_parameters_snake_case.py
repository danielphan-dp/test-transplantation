def test_get_value_from_session(app, client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_not_set(app, client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_empty_string(app, client):
    with client.session_transaction() as session:
        session['value'] = ''
    
    response = client.get('/get')
    assert response.data == b''

def test_get_value_none_type(app, client):
    with client.session_transaction() as session:
        session['value'] = None
    
    response = client.get('/get')
    assert response.data == b'None'