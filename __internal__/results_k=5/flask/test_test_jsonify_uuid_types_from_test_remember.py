import flask
import pytest

def test_get_value_from_session(app, client):
    """Test getting value from session"""

    with client.session_transaction() as session:
        session['value'] = 'test_value'

    rv = client.get('/get')
    assert rv.data.decode() == 'test_value'

def test_get_value_from_session_default(app, client):
    """Test getting default value when session key does not exist"""

    rv = client.get('/get')
    assert rv.data.decode() == 'None'

def test_get_value_from_session_empty(app, client):
    """Test getting empty value from session"""

    with client.session_transaction() as session:
        session['value'] = ''

    rv = client.get('/get')
    assert rv.data.decode() == ''