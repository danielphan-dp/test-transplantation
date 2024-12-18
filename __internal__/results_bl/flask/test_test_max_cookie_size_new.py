import flask
import pytest

@pytest.fixture
def set_session_value(app, client):
    with app.app_context():
        flask.session['value'] = 'test_value'
        yield
        flask.session.clear()

def test_get_with_value(set_session_value, app, client):
    response = client.get('/get')
    assert response.data.decode() == 'test_value'

def test_get_with_none_value(app, client):
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_with_empty_session(app, client):
    with app.app_context():
        flask.session.clear()
    response = client.get('/get')
    assert response.data.decode() == 'None'