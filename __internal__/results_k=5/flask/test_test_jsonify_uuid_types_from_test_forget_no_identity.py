import flask
import pytest

def test_get_value_from_session(app, client):
    """Test getting value from session"""

    with client.session_transaction() as session:
        session['value'] = 'test_value'

    rv = client.get('/get')
    assert rv.data.decode() == 'test_value'

def test_get_value_not_set(app, client):
    """Test getting value from session when not set"""

    rv = client.get('/get')
    assert rv.data.decode() == 'None'

def test_get_value_none(app, client):
    """Test getting value from session when explicitly set to None"""

    with client.session_transaction() as session:
        session['value'] = None

    rv = client.get('/get')
    assert rv.data.decode() == 'None'