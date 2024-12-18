import flask
import pytest

@pytest.mark.parametrize('session_value, expected', [
    (None, 'None'),
    ('test_value', 'test_value'),
])
def test_get_method_with_session_value(session_value, expected):
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    
    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    with app.test_request_context():
        flask.session['value'] = session_value
        client = app.test_client()
        response = client.get('/get')
        assert response.data.decode() == expected

def test_get_method_without_session_value():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    
    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    client = app.test_client()
    response = client.get('/get')
    assert response.data.decode() == 'None'