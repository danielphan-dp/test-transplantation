def test_get_value_from_session(app, client):
    with app.test_request_context():
        flask.session['value'] = 'Test Value'
        response = client.get('/get')
        assert response.data.decode() == 'Test Value'
        assert response.status_code == 200

def test_get_value_not_set(app, client):
    with app.test_request_context():
        response = client.get('/get')
        assert response.data.decode() == 'None'
        assert response.status_code == 200

def test_get_value_empty_string(app, client):
    with app.test_request_context():
        flask.session['value'] = ''
        response = client.get('/get')
        assert response.data.decode() == ''
        assert response.status_code == 200

def test_get_value_none_type(app, client):
    with app.test_request_context():
        flask.session['value'] = None
        response = client.get('/get')
        assert response.data.decode() == 'None'
        assert response.status_code == 200

def test_get_value_after_clear_session(app, client):
    with app.test_request_context():
        flask.session['value'] = 'Another Value'
        flask.session.clear()
        response = client.get('/get')
        assert response.data.decode() == 'None'
        assert response.status_code == 200