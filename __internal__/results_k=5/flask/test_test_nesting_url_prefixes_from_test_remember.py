import pytest
import flask

@pytest.mark.parametrize('session_value, expected', [
    ('test_value', 'test_value'),
    (None, 'None'),
    ('', ''),
])
def test_get_value_from_session(app, client, session_value, expected):
    with app.test_request_context():
        flask.session['value'] = session_value
        response = client.get('/get')
        assert response.data.decode() == expected

@pytest.mark.parametrize('session_value', [
    'another_value',
    'value_with_special_chars_!@#$%^&*()',
])
def test_get_value_with_special_characters(app, client, session_value):
    with app.test_request_context():
        flask.session['value'] = session_value
        response = client.get('/get')
        assert response.data.decode() == session_value

def test_get_value_without_session(app, client):
    response = client.get('/get')
    assert response.data.decode() == 'None'