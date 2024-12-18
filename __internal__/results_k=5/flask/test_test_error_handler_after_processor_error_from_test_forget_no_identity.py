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
        session['value'] = 'Test Value'
    rv = client.get('/get')
    assert rv.data == b'Test Value'

def test_get_session_value_empty(client):
    with client.session_transaction() as session:
        session['value'] = ''
    rv = client.get('/get')
    assert rv.data == b''

def test_get_session_value_nonexistent(client):
    rv = client.get('/get')
    assert rv.data == b'None'  # Testing default value when session key does not exist

def test_get_session_value_after_error(client):
    @app.route('/error')
    def error_route():
        raise ZeroDivisionError

    @app.errorhandler(500)
    def internal_server_error(e):
        return "Hello Server Error", 500

    rv = client.get('/error')
    assert rv.status_code == 500
    assert rv.data == b"Hello Server Error"  # Ensure error handling works without affecting session state

def test_get_session_value_with_multiple_requests(client):
    with client.session_transaction() as session:
        session['value'] = 'First Value'
    rv1 = client.get('/get')
    assert rv1.data == b'First Value'

    with client.session_transaction() as session:
        session['value'] = 'Second Value'
    rv2 = client.get('/get')
    assert rv2.data == b'Second Value'