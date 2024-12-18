import flask
import pytest
from werkzeug.exceptions import BadRequest

@pytest.mark.parametrize(('session_value', 'expected_response'), [
    (None, b'None'),
    ('test_value', b'test_value'),
    ('', b''),
])
def test_get_session_value(app, client, session_value, expected_response):
    with app.test_request_context():
        flask.session['value'] = session_value
        response = client.get('/get')
        assert response.data == expected_response
        assert response.status_code == 200

def test_get_session_value_no_session(app, client):
    response = client.get('/get')
    assert response.data == b'None'
    assert response.status_code == 200

def test_get_session_value_empty_string(app, client):
    with app.test_request_context():
        flask.session['value'] = ''
        response = client.get('/get')
        assert response.data == b''
        assert response.status_code == 200

def test_get_session_value_large_string(app, client):
    with app.test_request_context():
        flask.session['value'] = 'x' * 10000
        response = client.get('/get')
        assert response.data == b'x' * 10000
        assert response.status_code == 200

def test_get_session_value_special_characters(app, client):
    with app.test_request_context():
        flask.session['value'] = 'value_with_special_chars_!@#$%^&*()'
        response = client.get('/get')
        assert response.data == b'value_with_special_chars_!@#$%^&*()'
        assert response.status_code == 200