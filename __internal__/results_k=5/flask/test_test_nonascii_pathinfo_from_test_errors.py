def test_get_value_from_session(app, client):
    with client.session_transaction() as session:
        session['value'] = 'Test Value'
    
    rv = client.get('/get')
    assert rv.data == b'Test Value'

def test_get_value_not_set(app, client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_with_nonascii(app, client):
    with client.session_transaction() as session:
        session['value'] = 'Тестовое значение'
    
    rv = client.get('/get')
    assert rv.data == b'Тестовое значение'

def test_get_value_after_clear_session(app, client):
    with client.session_transaction() as session:
        session['value'] = 'Another Value'
    
    with client.session_transaction() as session:
        session.clear()
    
    rv = client.get('/get')
    assert rv.data == b'None'