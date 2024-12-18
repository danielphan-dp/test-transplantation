import flask
import pytest

def test_get_value_from_session(app, client):
    """Test getting value from session"""

    with client.session_transaction() as session:
        session['value'] = 'test_value'

    rv = client.get('/get')
    assert rv.data.decode() == 'test_value'

def test_get_value_from_empty_session(app, client):
    """Test getting value from an empty session"""

    rv = client.get('/get')
    assert rv.data.decode() == 'None'

def test_get_value_from_session_with_none(app, client):
    """Test getting value from session when value is None"""

    with client.session_transaction() as session:
        session['value'] = None

    rv = client.get('/get')
    assert rv.data.decode() == 'None'