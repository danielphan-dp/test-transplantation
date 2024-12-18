import pytest
import flask

def test_get_value_from_session(app):
    app.secret_key = 'test_secret'
    client = app.test_client()

    # Test default value when session is empty
    response = client.get('/get')
    assert response.data == b'None'

    # Test setting a value in the session
    with client.session_transaction() as session:
        session['value'] = 'test_value'

    # Test retrieving the value from the session
    response = client.get('/get')
    assert response.data == b'test_value'

    # Test clearing the session
    with client.session_transaction() as session:
        session.clear()

    # Test default value again after clearing session
    response = client.get('/get')
    assert response.data == b'None'