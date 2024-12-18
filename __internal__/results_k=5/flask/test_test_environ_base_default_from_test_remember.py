import flask
import pytest

def test_get_value_from_session(app, client):
    with client:
        # Test default value when session is empty
        response = client.get('/get')
        assert response.data.decode() == 'None'

        # Test setting a value in the session
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data.decode() == 'test_value'

        # Test clearing the session
        flask.session.clear()
        response = client.get('/get')
        assert response.data.decode() == 'None'