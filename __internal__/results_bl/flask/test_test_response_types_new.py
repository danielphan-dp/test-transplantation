def test_get_value(app, client):
    with app.test_request_context():
        flask.session['value'] = 'Test Value'
        rv = client.get('/get')
        assert rv.data.decode() == 'Test Value'
    
    with app.test_request_context():
        flask.session.clear()
        rv = client.get('/get')
        assert rv.data.decode() == 'None'
    
    with app.test_request_context():
        flask.session['value'] = None
        rv = client.get('/get')
        assert rv.data.decode() == 'None'