import pytest
from flask import Flask, session
from werkzeug.exceptions import BadRequest

app = Flask(__name__)
app.secret_key = 'test_secret'

@app.route('/get')
def get():
    v = session.get('value', 'None')
    return v

@pytest.mark.parametrize(('value', 'expected'), [
    (None, 'None'),
    ('test_value', 'test_value'),
    ('', ''),
])
def test_get_value(app, client, value, expected):
    with app.test_request_context():
        session['value'] = value
        rv = client.get('/get')
        assert rv.data.decode() == expected

def test_get_value_no_session(app, client):
    rv = client.get('/get')
    assert rv.data.decode() == 'None'