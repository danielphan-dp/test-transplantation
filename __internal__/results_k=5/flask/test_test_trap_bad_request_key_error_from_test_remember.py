import flask
import pytest
from werkzeug.exceptions import BadRequest

@pytest.mark.parametrize(('session_value', 'expected_response'), [
    (None, 'None'),
    ('test_value', 'test_value'),
    ('', ''),
])
def test_get_value_from_session(app, client, session_value, expected_response):
    with app.test_request_context():
        flask.session['value'] = session_value
        response = client.get('/get')
        assert response.data.decode() == expected_response

def test_get_value_no_session(app, client):
    with app.test_request_context():
        response = client.get('/get')
        assert response.data.decode() == 'None'