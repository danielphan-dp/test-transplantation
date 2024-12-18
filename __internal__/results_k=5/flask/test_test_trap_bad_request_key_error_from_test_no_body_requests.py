import flask
import pytest

@pytest.mark.parametrize(('session_value', 'expected_response'), [
    (None, 'None'),
    ('test_value', 'test_value'),
    ('', ''),
])
def test_get_session_value(app, client, session_value, expected_response):
    with app.test_request_context():
        flask.session['value'] = session_value
        response = client.get('/get')
        assert response.data.decode() == expected_response
        assert response.status_code == 200

def test_get_session_value_no_session(app, client):
    response = client.get('/get')
    assert response.data.decode() == 'None'
    assert response.status_code == 200

def test_get_session_value_empty_session(app, client):
    with app.test_request_context():
        flask.session['value'] = ''
        response = client.get('/get')
        assert response.data.decode() == ''
        assert response.status_code == 200