import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_value_from_session(client, app):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        rv = client.get('/get')
        assert rv.data.decode() == 'test_value'
        assert rv.status_code == 200

def test_get_value_not_set(client, app):
    with app.test_request_context():
        rv = client.get('/get')
        assert rv.data.decode() == 'None'
        assert rv.status_code == 200

def test_get_value_empty_string(client, app):
    with app.test_request_context():
        flask.session['value'] = ''
        rv = client.get('/get')
        assert rv.data.decode() == ''
        assert rv.status_code == 200

def test_get_value_none(client, app):
    with app.test_request_context():
        flask.session['value'] = None
        rv = client.get('/get')
        assert rv.data.decode() == 'None'
        assert rv.status_code == 200