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

def test_get_session_value_nonexistent_key(client):
    rv = client.get('/get')
    assert rv.data == b'None'  # Testing default value when key does not exist

def test_get_session_value_after_error(client):
    @app.route('/error')
    def error_route():
        raise ZeroDivisionError

    @app.errorhandler(500)
    def internal_server_error(e):
        return "Hello Server Error", 500

    rv = client.get('/error')
    assert rv.status_code == 500
    assert rv.data == b"Hello Server Error"  # Ensure error handling works without affecting session

def test_get_session_value_with_multiple_requests(client):
    with client.session_transaction() as session:
        session['value'] = 'first_value'
    rv1 = client.get('/get')
    assert rv1.data == b'first_value'

    with client.session_transaction() as session:
        session['value'] = 'second_value'
    rv2 = client.get('/get')
    assert rv2.data == b'second_value'