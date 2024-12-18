import flask
import pytest

def test_get_value_none(app, client):
    """Test that the default value is returned when session value is not set."""
    rv = client.get('/get')
    assert rv.data == b'None'
    assert rv.mimetype == 'text/html'

def test_get_value_set(app, client):
    """Test that the correct value is returned when session value is set."""
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    rv = client.get('/get')
    assert rv.data == b'test_value'
    assert rv.mimetype == 'text/html'

def test_get_value_empty_string(app, client):
    """Test that an empty string is returned when session value is set to an empty string."""
    with client.session_transaction() as session:
        session['value'] = ''
    rv = client.get('/get')
    assert rv.data == b''
    assert rv.mimetype == 'text/html'

def test_get_value_none_type(app, client):
    """Test that None is returned when session value is explicitly set to None."""
    with client.session_transaction() as session:
        session['value'] = None
    rv = client.get('/get')
    assert rv.data == b'None'
    assert rv.mimetype == 'text/html'