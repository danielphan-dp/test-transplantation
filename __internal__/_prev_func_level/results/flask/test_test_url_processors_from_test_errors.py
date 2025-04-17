def test_get_value(app, client):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data == b'test_value'

    with app.test_request_context():
        flask.session.clear()
        response = client.get('/get')
        assert response.data == b'None'

    with app.test_request_context():
        flask.session['value'] = None
        response = client.get('/get')
        assert response.data == b'None'