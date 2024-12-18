import pytest
import flask

def test_get_value_from_session(app, client, app_ctx):
    @app.route("/setvalue", methods=["POST"])
    def set_value():
        flask.session['value'] = 'test_value'
        return "Value set"

    with client:
        # Test default value when session is empty
        rv = client.get('/get')
        assert rv.data == b'None'

        # Set a value in the session and test retrieval
        client.post('/setvalue')
        rv = client.get('/get')
        assert rv.data == b'test_value'

        # Clear the session and test retrieval again
        with client.session_transaction() as sess:
            sess.clear()
        rv = client.get('/get')
        assert rv.data == b'None'

        # Test with a different value
        @app.route("/setanothervalue", methods=["POST"])
        def set_another_value():
            flask.session['value'] = 'another_value'
            return "Another value set"

        client.post('/setanothervalue')
        rv = client.get('/get')
        assert rv.data == b'another_value'