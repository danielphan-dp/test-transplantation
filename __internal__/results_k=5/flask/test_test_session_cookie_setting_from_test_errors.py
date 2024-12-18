import flask
import pytest

def test_get_session_value(app):
    @app.route("/set")
    def set_value():
        flask.session['value'] = 'test_value'
        return "Value set"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    with app.test_client() as c:
        # Test default value when session is empty
        response = c.get("/get")
        assert response.data == b'None'

        # Set a value in the session
        c.get("/set")

        # Test retrieving the set value
        response = c.get("/get")
        assert response.data == b'test_value'

        # Test session persistence
        response = c.get("/get")
        assert response.data == b'test_value'

        # Clear session and test again
        with flask.session_transaction() as sess:
            sess.clear()
        
        response = c.get("/get")
        assert response.data == b'None'