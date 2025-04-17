import flask
import pytest

def test_get_value_from_session(app, client):
    app.testing = True

    @app.route("/set")
    def set_value():
        flask.session['value'] = 'Test Value'
        return "Value Set"

    with client:
        resp = client.get("/set")
        assert resp.data == b"Value Set"
        assert resp.status_code == 200

    with client:
        resp = client.get('/get')
        assert resp.data == b'Test Value'
        assert resp.status_code == 200

def test_get_value_not_set(app, client):
    app.testing = True

    with client:
        resp = client.get('/get')
        assert resp.data == b'None'
        assert resp.status_code == 200

def test_get_value_empty_session(app, client):
    app.testing = True
    app.secret_key = 'test_secret'

    with client:
        resp = client.get('/get')
        assert resp.data == b'None'
        assert resp.status_code == 200

    with client:
        flask.session['value'] = ''
        resp = client.get('/get')
        assert resp.data == b''
        assert resp.status_code == 200

def test_get_value_none_type(app, client):
    app.testing = True
    app.secret_key = 'test_secret'

    with client:
        flask.session['value'] = None
        resp = client.get('/get')
        assert resp.data == b'None'
        assert resp.status_code == 200