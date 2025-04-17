import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_value_from_session(client):
    with client:
        flask.session['value'] = 'test_value'
        rv = client.get('/get')
        assert rv.data.decode() == 'test_value'

def test_get_value_not_set(client):
    with client:
        rv = client.get('/get')
        assert rv.data.decode() == 'None'

def test_get_value_after_clear(client):
    with client:
        flask.session['value'] = 'test_value'
        flask.session.clear()
        rv = client.get('/get')
        assert rv.data.decode() == 'None'