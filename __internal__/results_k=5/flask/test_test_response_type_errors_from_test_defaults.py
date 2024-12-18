import flask
import pytest

app = flask.Flask(__name__)
app.testing = True

@app.route('/get')
def get():
    v = flask.session.get('value', 'None')
    return v

def test_get_with_no_session_value():
    c = app.test_client()
    response = c.get('/get')
    assert response.data == b'None'

def test_get_with_session_value():
    with app.test_client() as c:
        with c.session_transaction() as session:
            session['value'] = 'Test Value'
        response = c.get('/get')
        assert response.data == b'Test Value'

def test_get_with_empty_session_value():
    with app.test_client() as c:
        with c.session_transaction() as session:
            session['value'] = ''
        response = c.get('/get')
        assert response.data == b''

def test_get_with_none_session_value():
    with app.test_client() as c:
        with c.session_transaction() as session:
            session['value'] = None
        response = c.get('/get')
        assert response.data == b'None'