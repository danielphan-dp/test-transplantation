import pytest
import flask

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_route_with_value_in_session(app, client):
    with app.app_context():
        flask.session['value'] = 'test_value'
    response = client.get('/get')
    assert response.data.decode() == 'test_value'

def test_get_route_with_no_value_in_session(app, client):
    with app.app_context():
        flask.session.clear()
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_route_with_none_value_in_session(app, client):
    with app.app_context():
        flask.session['value'] = None
    response = client.get('/get')
    assert response.data.decode() == 'None'