import flask
import pytest

app = flask.Flask(__name__)
app.testing = True

@app.route('/get')
def get():
    v = flask.session.get('value', 'None')
    return v

def test_get_with_default_value():
    c = app.test_client()
    response = c.get('/get')
    assert response.data == b'None'

def test_get_with_set_value():
    with app.test_request_context():
        flask.session['value'] = 'Test Value'
    c = app.test_client()
    response = c.get('/get')
    assert response.data == b'Test Value'

def test_get_with_empty_session():
    with app.test_request_context():
        flask.session.clear()
    c = app.test_client()
    response = c.get('/get')
    assert response.data == b'None'

def test_get_with_none_value():
    with app.test_request_context():
        flask.session['value'] = None
    c = app.test_client()
    response = c.get('/get')
    assert response.data == b'None'