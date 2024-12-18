def test_get_value_from_session(test_apps):
    from blueprintapp import app
    import flask

    client = app.test_client()

    # Test when session is empty
    with app.test_request_context():
        flask.session.clear()
        rv = client.get('/get')
        assert rv.data == b'None'

    # Test when session has a value
    with app.test_request_context():
        flask.session['value'] = 'Test Value'
        rv = client.get('/get')
        assert rv.data == b'Test Value'

    # Test when session is set to None
    with app.test_request_context():
        flask.session['value'] = None
        rv = client.get('/get')
        assert rv.data == b'None'

    # Test with a different session value
    with app.test_request_context():
        flask.session['value'] = 'Another Value'
        rv = client.get('/get')
        assert rv.data == b'Another Value'