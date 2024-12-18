def test_get_value_from_session(app, client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_value_from_session_default(app, client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_from_session_empty(app, client):
    with client.session_transaction() as session:
        session['value'] = ''
    
    rv = client.get('/get')
    assert rv.data == b''

def test_get_value_from_session_none(app, client):
    with client.session_transaction() as session:
        session['value'] = None
    
    rv = client.get('/get')
    assert rv.data == b'None'