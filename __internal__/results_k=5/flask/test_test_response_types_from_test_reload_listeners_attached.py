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

    # Test when session is empty
    with client.session_transaction() as sess:
        sess.clear()
    rv = client.get("/get")
    assert rv.data == b'None'
    assert rv.status_code == 200

    # Test with a different value
    @app.route("/set_another_value")
    def set_another_value():
        flask.session['value'] = 'Another Value'
        return "Another Value Set"

    client.get("/set_another_value")
    rv = client.get("/get")
    assert rv.data == b'Another Value'
    assert rv.status_code == 200