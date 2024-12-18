import pytest
from werkzeug.exceptions import InternalServerError
from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'test_secret'

@app.route('/get')
def get():
    v = session.get('value', 'None')
    return v

@pytest.mark.parametrize('to_handle', (InternalServerError, 500))
def test_get_value_none(app, client, to_handle):
    with app.test_request_context():
        response = client.get('/get')
        assert response.data == b'None'

@pytest.mark.parametrize('to_handle', (InternalServerError, 500))
def test_get_value_set(app, client, to_handle):
    with app.test_request_context():
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['value'] = 'test_value'
            response = client.get('/get')
            assert response.data == b'test_value'

@pytest.mark.parametrize('to_handle', (InternalServerError, 500))
def test_get_value_empty(app, client, to_handle):
    with app.test_request_context():
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['value'] = ''
            response = client.get('/get')
            assert response.data == b''

@pytest.mark.parametrize('to_handle', (InternalServerError, 500))
def test_get_value_none_with_session(app, client, to_handle):
    with app.test_request_context():
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['value'] = None
            response = client.get('/get')
            assert response.data == b'None'