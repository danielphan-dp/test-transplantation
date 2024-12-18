import flask
import pytest

@pytest.mark.parametrize('value, expected', [
    (None, 'None'),
    ('test_value', 'test_value'),
])
def test_get_value(app, client, value, expected):
    with app.app_context():
        flask.session['value'] = value
    response = client.get('/get')
    assert response.data.decode() == expected
    assert response.status_code == 200

def test_get_value_no_session(app, client):
    response = client.get('/get')
    assert response.data.decode() == 'None'
    assert response.status_code == 200

def test_get_value_empty_string(app, client):
    with app.app_context():
        flask.session['value'] = ''
    response = client.get('/get')
    assert response.data.decode() == ''
    assert response.status_code == 200

def test_get_value_special_characters(app, client):
    with app.app_context():
        flask.session['value'] = '!@#$%^&*()'
    response = client.get('/get')
    assert response.data.decode() == '!@#$%^&*()'
    assert response.status_code == 200