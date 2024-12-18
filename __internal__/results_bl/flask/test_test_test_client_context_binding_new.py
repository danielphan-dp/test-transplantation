import pytest
import flask

def test_get_value_from_session(app, client):
    app.testing = True
    with client:
        # Test when session has a value
        with client.session_transaction() as session:
            session['value'] = 'Test Value'
        resp = client.get('/get')
        assert resp.data == b'Test Value'
        assert resp.status_code == 200

def test_get_value_default(app, client):
    app.testing = True
    with client:
        # Test when session does not have a value
        resp = client.get('/get')
        assert resp.data == b'None'
        assert resp.status_code == 200

def test_get_value_empty_string(app, client):
    app.testing = True
    with client:
        # Test when session has an empty string as value
        with client.session_transaction() as session:
            session['value'] = ''
        resp = client.get('/get')
        assert resp.data == b''
        assert resp.status_code == 200

def test_get_value_none_type(app, client):
    app.testing = True
    with client:
        # Test when session has None as value
        with client.session_transaction() as session:
            session['value'] = None
        resp = client.get('/get')
        assert resp.data == b'None'
        assert resp.status_code == 200