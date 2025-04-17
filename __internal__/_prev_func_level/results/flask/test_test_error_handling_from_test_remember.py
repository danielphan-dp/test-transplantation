def test_get_value_from_session(app, client):
    app.testing = True

    @app.route("/set/<value>")
    def set_value(value):
        flask.session['value'] = value
        return "Value set"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    # Test default session value
    rv = client.get("/get")
    assert rv.data == b'None'

    # Test setting and getting a session value
    rv = client.get("/set/test_value")
    assert rv.data == b'Value set'
    
    rv = client.get("/get")
    assert rv.data == b'test_value'

    # Test setting another session value
    rv = client.get("/set/another_value")
    assert rv.data == b'Value set'
    
    rv = client.get("/get")
    assert rv.data == b'another_value'