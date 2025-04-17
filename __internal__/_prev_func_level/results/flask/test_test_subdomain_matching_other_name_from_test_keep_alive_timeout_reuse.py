import flask
import pytest

@pytest.mark.parametrize('session_value, expected', [
    (None, 'None'),
    ('test_value', 'test_value'),
])
def test_get_session_value(session_value, expected):
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    client = app.test_client()

    with app.app_context():
        flask.session['value'] = session_value

    response = client.get('/get')
    assert response.data.decode() == expected
    assert response.status_code == 200

def test_get_session_value_no_session():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    client = app.test_client()

    response = client.get('/get')
    assert response.data.decode() == 'None'
    assert response.status_code == 200