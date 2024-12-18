import flask
from flask.globals import request_ctx
from flask.sessions import SessionInterface
import pytest

app = flask.Flask(__name__)

class MySessionInterface(SessionInterface):
    def save_session(self, app, session, response):
        pass

    def open_session(self, app, request):
        request_ctx.match_request()
        return super().open_session(app, request)

app.session_interface = MySessionInterface()

@app.route('/get')
def get():
    v = flask.session.get('value', 'None')
    return v

def test_get_with_default_value():
    with app.test_client() as client:
        response = client.get('/get')
        assert response.data.decode() == 'None'
        assert response.status_code == 200

def test_get_with_set_value():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['value'] = 'Test Value'
        response = client.get('/get')
        assert response.data.decode() == 'Test Value'
        assert response.status_code == 200

def test_get_with_empty_session():
    with app.test_client() as client:
        response = client.get('/get')
        assert response.data.decode() == 'None'
        assert response.status_code == 200

def test_get_with_none_value():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['value'] = None
        response = client.get('/get')
        assert response.data.decode() == 'None'
        assert response.status_code == 200

def test_get_with_nonexistent_key():
    with app.test_client() as client:
        response = client.get('/get')
        assert response.data.decode() == 'None'
        assert response.status_code == 200