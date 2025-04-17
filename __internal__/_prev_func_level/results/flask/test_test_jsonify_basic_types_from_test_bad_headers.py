import flask
import pytest

@pytest.mark.parametrize('session_value, expected', [
    ('test_value', 'test_value'),
    (None, 'None'),
    ('', ''),
    ('long string', 'long string'),
    (123, '123'),
    (True, 'True'),
    (False, 'False'),
])
def test_get_session_value(session_value, expected, app, client):
    with app.test_request_context():
        flask.session['value'] = session_value
        response = client.get('/get')
        assert response.data.decode() == expected
        assert response.mimetype == 'text/html'  # Assuming default mimetype for Flask responses