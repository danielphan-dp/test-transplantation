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

    # Test when session has a different value
    with app.test_request_context():
        flask.session['value'] = 'Another Value'
        rv = client.get('/get')
        assert rv.data == b'Another Value'

    # Test session persistence across requests
    with app.test_request_context():
        flask.session['value'] = 'Persistent Value'
    rv = client.get('/get')
    assert rv.data == b'Persistent Value'

    # Test session after clearing
    with app.test_request_context():
        flask.session.clear()
        rv = client.get('/get')
        assert rv.data == b'None'