import flask
import pytest
from werkzeug.exceptions import BadRequest

@pytest.mark.parametrize(('session_value', 'expected_response'), [
    (None, b'None'),
    ('test_value', b'test_value'),
    ('', b''),
])
def test_get_value_from_session(app, client, session_value, expected_response):
    with app.test_request_context():
        flask.session['value'] = session_value
        response = client.get('/get')
        assert response.data == expected_response
        assert response.status_code == 200

def test_get_value_no_session(app, client):
    response = client.get('/get')
    assert response.data == b'None'
    assert response.status_code == 200

def test_get_value_with_invalid_session(app, client):
    with app.test_request_context():
        flask.session['value'] = object()  # Assigning a non-serializable object
        response = client.get('/get')
        assert response.data == b'None'
        assert response.status_code == 200