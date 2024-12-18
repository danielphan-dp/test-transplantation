def test_get_value(app, client):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        rv = client.get('/get')
        assert rv.data == b'test_value'

def test_get_value_none(app, client):
    with app.test_request_context():
        rv = client.get('/get')
        assert rv.data == b'None'

def test_get_value_empty(app, client):
    with app.test_request_context():
        flask.session['value'] = ''
        rv = client.get('/get')
        assert rv.data == b''