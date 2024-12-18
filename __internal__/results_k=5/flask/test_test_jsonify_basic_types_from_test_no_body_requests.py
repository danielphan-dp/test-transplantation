import flask
import pytest

@pytest.mark.parametrize('session_value, expected', [
    ('test_value', 'test_value'),
    (None, 'None'),
    ('', ''),
    (123, '123'),
    (True, 'True'),
    (False, 'False'),
])
def test_get_session_value(session_value, expected, app, client):
    with app.test_request_context():
        flask.session['value'] = session_value
    rv = client.get('/get')
    assert rv.data.decode() == expected
    assert rv.mimetype == 'text/html; charset=utf-8'