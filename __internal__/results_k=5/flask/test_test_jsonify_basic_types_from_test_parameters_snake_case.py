import flask
import pytest

@pytest.mark.parametrize('session_value, expected', [
    ('test_value', 'test_value'),
    (None, 'None'),
    ('', ''),
    ('123', '123'),
    ('True', 'True'),
    ('False', 'False'),
])
def test_get_session_value(session_value, expected, app, client):
    with app.test_request_context():
        flask.session['value'] = session_value
        response = client.get('/get')
        assert response.data.decode() == expected
        assert response.mimetype == 'text/html'  # Flask default mimetype for string responses

def test_get_session_value_no_session(app, client):
    response = client.get('/get')
    assert response.data.decode() == 'None'
    assert response.mimetype == 'text/html'  # Flask default mimetype for string responses

def test_get_session_value_empty_string(app, client):
    with app.test_request_context():
        flask.session['value'] = ''
        response = client.get('/get')
        assert response.data.decode() == ''
        assert response.mimetype == 'text/html'  # Flask default mimetype for string responses

def test_get_session_value_numeric_string(app, client):
    with app.test_request_context():
        flask.session['value'] = '456'
        response = client.get('/get')
        assert response.data.decode() == '456'
        assert response.mimetype == 'text/html'  # Flask default mimetype for string responses