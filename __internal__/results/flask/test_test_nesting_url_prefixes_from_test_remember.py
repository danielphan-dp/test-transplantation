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
    'test_value',
    None,
    '',
])
def test_get_value_default(app, client, session_value):
    with app.test_request_context():
        if session_value is not None:
            flask.session['value'] = session_value
        else:
            flask.session.pop('value', None)
        response = client.get('/get')
        assert response.data.decode() == (session_value if session_value is not None else 'None')