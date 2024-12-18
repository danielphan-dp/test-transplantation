import flask
import pytest

def test_get_method(app):
    @app.route("/set_value/<value>")
    def set_value(value):
        flask.session['value'] = value
        return "Value set"

    with app.test_client() as c:
        # Test default value when session is empty
        response = c.get('/get')
        assert response.data == b'None'

        # Test setting a value in the session
        c.get('/set_value/test_value')
        response = c.get('/get')
        assert response.data == b'test_value'

        # Test setting a different value in the session
        c.get('/set_value/another_value')
        response = c.get('/get')
        assert response.data == b'another_value'

        # Test clearing the session
        with flask.session_transaction() as sess:
            sess.clear()
        response = c.get('/get')
        assert response.data == b'None'