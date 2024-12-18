import flask
import pytest

def test_get_with_no_session_value(app, client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_with_empty_session_value(app, client):
    with client.session_transaction() as session:
        session['value'] = ''
    response = client.get('/get')
    assert response.data == b''

def test_get_with_none_session_value(app, client):
    with client.session_transaction() as session:
        session['value'] = None
    response = client.get('/get')
    assert response.data == b'None'

def test_get_after_setting_value(app, client):
    assert client.post('/set', data={'value': '100'}).data == b'value set'
    response = client.get('/get')
    assert response.data == b'100'

def test_get_session_accessed_flag(app, client):
    assert client.post('/set', data={'value': '200'}).data == b'value set'
    with client.session_transaction() as session:
        assert not session.accessed
    response = client.get('/get')
    with client.session_transaction() as session:
        assert session.accessed
    assert response.data == b'200'