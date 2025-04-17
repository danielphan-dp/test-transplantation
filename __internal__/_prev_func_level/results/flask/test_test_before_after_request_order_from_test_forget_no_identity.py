import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_session_value_none(client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_session_value_set(client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_session_value_empty_string(client):
    with client.session_transaction() as session:
        session['value'] = ''
    rv = client.get('/get')
    assert rv.data == b''

def test_get_session_value_nonexistent(client):
    rv = client.get('/get')
    assert rv.data == b'None'  # Testing default value when session key does not exist

def test_get_session_value_after_request_order(client):
    called = []

    @app.before_request
    def before1():
        called.append(1)

    @app.after_request
    def after1(response):
        called.append(2)
        return response

    rv = client.get('/get')
    assert rv.data == b'None'
    assert called == [1, 2]  # Ensure before and after request order is correct