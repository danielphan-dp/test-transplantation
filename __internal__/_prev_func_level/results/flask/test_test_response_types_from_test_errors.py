def test_get_value_from_session(app, client):
    with client.session_transaction() as session:
        session['value'] = 'Test Value'
    
    rv = client.get('/get')
    assert rv.data.decode() == 'Test Value'
    assert rv.status_code == 200

def test_get_value_not_set(app, client):
    rv = client.get('/get')
    assert rv.data.decode() == 'None'
    assert rv.status_code == 200

def test_get_value_with_different_session(app, client):
    with client.session_transaction() as session:
        session['value'] = 'Another Value'
    
    rv = client.get('/get')
    assert rv.data.decode() == 'Another Value'
    assert rv.status_code == 200

def test_get_value_after_session_clear(app, client):
    with client.session_transaction() as session:
        session['value'] = 'Value Before Clear'
    
    with client.session_transaction() as session:
        session.clear()
    
    rv = client.get('/get')
    assert rv.data.decode() == 'None'
    assert rv.status_code == 200

def test_get_value_with_non_string(app, client):
    with client.session_transaction() as session:
        session['value'] = 12345
    
    rv = client.get('/get')
    assert rv.data.decode() == '12345'
    assert rv.status_code == 200