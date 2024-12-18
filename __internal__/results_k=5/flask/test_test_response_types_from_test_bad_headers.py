def test_get_value_from_session(app, client):
    @app.route("/set_value")
    def set_value():
        flask.session['value'] = 'Test Value'
        return 'Value Set'

    @app.route("/clear_value")
    def clear_value():
        flask.session.pop('value', None)
        return 'Value Cleared'

    # Test setting a value in the session
    client.get("/set_value")
    rv = client.get("/get")
    assert rv.data.decode() == 'Test Value'

    # Test clearing the value from the session
    client.get("/clear_value")
    rv = client.get("/get")
    assert rv.data.decode() == 'None'

    # Test when session is empty
    with client.session_transaction() as sess:
        sess.clear()
    rv = client.get("/get")
    assert rv.data.decode() == 'None'