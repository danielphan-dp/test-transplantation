def test_get_session_value(app):
    @app.route("/set_value/<value>")
    def set_value(value):
        flask.session['value'] = value
        return "Value set"

    @app.route("/get_value")
    def get_value():
        return flask.session.get('value', 'None')

    with app.test_client() as c:
        # Test default value when session is empty
        rv = c.get("/get_value")
        assert rv.data == b'None'

        # Test setting a value in the session
        c.get("/set_value/test_value")
        rv = c.get("/get_value")
        assert rv.data == b'test_value'

        # Test setting another value in the session
        c.get("/set_value/another_value")
        rv = c.get("/get_value")
        assert rv.data == b'another_value'

        # Test clearing the session
        with flask.session_transaction() as sess:
            sess.clear()
        rv = c.get("/get_value")
        assert rv.data == b'None'