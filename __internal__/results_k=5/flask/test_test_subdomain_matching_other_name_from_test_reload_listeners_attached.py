import flask
import pytest

@pytest.mark.parametrize('session_value, expected', [
    (None, b'None'),
    ('test_value', b'test_value'),
])
def test_get_session_value(session_value, expected):
    app = flask.Flask(__name__)
    client = app.test_client()

    with app.app_context():
        flask.session['value'] = session_value

    response = client.get('/get')
    assert response.data == expected

def test_get_session_value_no_session():
    app = flask.Flask(__name__)
    client = app.test_client()

    response = client.get('/get')
    assert response.data == b'None'