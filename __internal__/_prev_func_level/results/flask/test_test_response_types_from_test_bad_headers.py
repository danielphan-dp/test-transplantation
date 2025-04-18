def test_get_value_from_session(app, client):
    @app.route("/set_value")
    def set_value():
        flask.session['value'] = 'Test Value'
        return "Value Set"

    @app.route("/clear_value")
    def clear_value():
        flask.session.pop('value', None)
        return "Value Cleared"

    # Test setting a value in the session
    client.get("/set_value")
    rv = client.get("/get")
    assert rv.data == b'Test Value'
    assert rv.status_code == 200

    # Test clearing the value from the session
    client.get("/clear_value")
    rv = client.get("/get")
    assert rv.data == b'None'
    assert rv.status_code == 200

    # Test getting value when session is empty
    with client.session_transaction() as sess:
        sess.clear()
    rv = client.get("/get")
    assert rv.data == b'None'
    assert rv.status_code == 200

    # Test setting a different value in the session
    with client.session_transaction() as sess:
        sess['value'] = 'Another Value'
    rv = client.get("/get")
    assert rv.data == b'Another Value'
    assert rv.status_code == 200