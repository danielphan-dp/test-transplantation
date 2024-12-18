import pytest
from werkzeug.exceptions import Forbidden, HTTPException, NotFound
import flask

app = flask.Flask(__name__)

@app.route('/get')
def get():
    v = flask.session.get('value', 'None')
    return v

def test_get_default_value():
    with app.test_client() as c:
        response = c.get('/get')
        assert response.data == b'None'

def test_get_with_session_value():
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['value'] = 'test_value'
        response = c.get('/get')
        assert response.data == b'test_value'

def test_get_with_empty_session():
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess.clear()
        response = c.get('/get')
        assert response.data == b'None'

def test_get_with_none_session_value():
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['value'] = None
        response = c.get('/get')
        assert response.data == b'None'