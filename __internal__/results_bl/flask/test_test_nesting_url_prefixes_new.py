import pytest
import flask
from blueprintapp.app import app

@pytest.mark.parametrize('session_value, expected_response', [
    ('test_value', 'test_value'),
    (None, 'None'),
    ('', ''),
])
def test_get_method(client, session_value, expected_response):
    with app.test_request_context():
        flask.session['value'] = session_value
        response = client.get('/get')
        assert response.data.decode() == expected_response

@pytest.mark.parametrize('session_value', [
    'another_value',
    'value_with_special_chars_!@#$%^&*()',
])
def test_get_method_with_special_values(client, session_value):
    with app.test_request_context():
        flask.session['value'] = session_value
        response = client.get('/get')
        assert response.data.decode() == session_value

def test_get_method_without_session(client):
    response = client.get('/get')
    assert response.data.decode() == 'None'