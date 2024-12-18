def test_get_value(app, client):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        rv = client.get('/get')
        assert rv.data == b'test_value'

    with app.test_request_context():
        flask.session.pop('value', None)
        rv = client.get('/get')
        assert rv.data == b'None'

    with app.test_request_context():
        flask.session['value'] = None
        rv = client.get('/get')
        assert rv.data == b'None'