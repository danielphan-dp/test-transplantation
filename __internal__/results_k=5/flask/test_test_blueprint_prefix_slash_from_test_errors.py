import pytest
import flask
from blueprintapp.app import app

@pytest.mark.parametrize(('value', 'expected'), [
    (None, 'None'),
    ('test_value', 'test_value'),
])
def test_get_value_from_session(app, client, value, expected):
    with app.app_context():
        flask.session['value'] = value
    response = client.get('/get')
    assert response.data.decode() == expected
    assert response.status_code == 200

def test_get_value_no_session(app, client):
    response = client.get('/get')
    assert response.data.decode() == 'None'
    assert response.status_code == 200

def test_get_value_empty_session(app, client):
    with app.app_context():
        flask.session.clear()
    response = client.get('/get')
    assert response.data.decode() == 'None'
    assert response.status_code == 200

def test_get_value_with_special_characters(app, client):
    with app.app_context():
        flask.session['value'] = 'value_with_special_chars_!@#$%^&*()'
    response = client.get('/get')
    assert response.data.decode() == 'value_with_special_chars_!@#$%^&*()'
    assert response.status_code == 200