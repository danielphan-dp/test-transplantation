import flask
import pytest

def test_get_value_from_session():
    app = flask.Flask(__name__)
    client = app.test_client()

    @app.route('/set/<value>')
    def set_value(value):
        flask.session['value'] = value
        return '', 204

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    with app.test_request_context():
        client.get('/set/test_value')
        response = client.get('/get')
        assert response.status_code == 200
        assert response.data == b'test_value'

def test_get_value_not_set():
    app = flask.Flask(__name__)
    client = app.test_client()

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    response = client.get('/get')
    assert response.status_code == 200
    assert response.data == b'None'