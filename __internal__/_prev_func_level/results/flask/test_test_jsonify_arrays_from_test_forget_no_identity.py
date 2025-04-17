import flask
import pytest

def test_get_session_value_none(app, client):
    """Test that the default session value is 'None' when not set."""
    with client.session_transaction() as session:
        session.clear()  # Ensure session is empty
    rv = client.get('/get')
    assert rv.data == b'None'
    assert rv.mimetype == 'text/html'

def test_get_session_value_set(app, client):
    """Test that the session value is returned correctly when set."""
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    rv = client.get('/get')
    assert rv.data == b'test_value'
    assert rv.mimetype == 'text/html'

def test_get_session_value_empty_string(app, client):
    """Test that an empty string is returned correctly when set as session value."""
    with client.session_transaction() as session:
        session['value'] = ''
    rv = client.get('/get')
    assert rv.data == b''
    assert rv.mimetype == 'text/html'

def test_get_session_value_none_after_clear(app, client):
    """Test that the session returns 'None' after clearing the session."""
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    with client.session_transaction() as session:
        session.clear()  # Clear the session
    rv = client.get('/get')
    assert rv.data == b'None'
    assert rv.mimetype == 'text/html'