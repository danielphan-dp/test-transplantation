import flask
import pytest
import warnings

@pytest.mark.parametrize('value, expected', [
    ('test_value', 'test_value'),
    (None, 'None'),
    ('', ''),
])
def test_get_with_session_value(value, expected):
    app = flask.Flask(__name__)
    app.config["SERVER_NAME"] = "localhost.localdomain:3000"
    client = app.test_client()
    
    with app.app_context():
        flask.session['value'] = value

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    rv = client.get('/get')
    assert rv.data.decode() == expected

def test_get_without_session_value():
    app = flask.Flask(__name__)
    app.config["SERVER_NAME"] = "localhost.localdomain:3000"
    client = app.test_client()

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    rv = client.get('/get')
    assert rv.data.decode() == 'None'