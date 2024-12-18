import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_session_value_none(client):
    rv = client.get('/get')
    assert rv.status_code == 200
    assert rv.data == b'None'

def test_get_session_value_set(client, app):
    with app.app_context():
        flask.session['value'] = 'test_value'
    rv = client.get('/get')
    assert rv.status_code == 200
    assert rv.data == b'test_value'

def test_get_session_value_empty(client, app):
    with app.app_context():
        flask.session['value'] = ''
    rv = client.get('/get')
    assert rv.status_code == 200
    assert rv.data == b''

def test_get_session_value_after_teardown(client, app):
    @app.teardown_request
    def teardown_request(exc):
        flask.session['value'] = 'teardown_value'

    with app.app_context():
        flask.session['value'] = 'initial_value'
    rv = client.get('/get')
    assert rv.status_code == 200
    assert rv.data == b'initial_value'  # Ensure the session value is not affected by teardown

    # Trigger teardown
    client.get('/get')
    assert flask.session.get('value') == 'initial_value'  # Check session value remains intact after request